import types
import inspect
import json


def prepare_func(func) -> dict:
    func_info_dict = {"py/function": func.__module__ + "." + func.__name__}

    func_globs = get_func_globals(func)
    for glob_name in func_globs:
        if isinstance(func_globs[glob_name], types.ModuleType):
            func_globs[glob_name] = "__module_name__"

    func_info_dict["__globals__"] = func_globs

    """all_members = inspect.getmembers(func.__code__)
    member_list = list(filter(lambda member: member[0].startswith("co_"), all_members))
    func_info_dict["__code__"] = get_func_code_info(member_list)"""

    return func_info_dict


def get_func_globals(func: types.FunctionType) -> dict:
    func_globs = func.__globals__
    needed_globs = func.__code__.co_names
    ret_globs = {}

    for glob in needed_globs:
        if glob in func_globs:
            ret_globs[glob] = func_globs[glob]

    return ret_globs


def get_func_code_info(member_list: list) -> dict:
    ret = "{\n"

    length = len(member_list)

    for i in range(0, length):
        member = member_list[i]
        key = member[0]
        value = member[1]
        ret += f'"{key}": '

        if isinstance(value, bytes):
            ret += f'"{value.hex()}"'
        else:
            ret += json.dumps(value)

        if i == length - 1:
            ret += "\n"
        else:
            ret += ",\n"

    ret += "}\n"
    return ret


"""
def dump_func_code_info(member_list: list) -> str:
    ret = "{\n"

    length = len(member_list)

    for i in range(0, length):
        member = member_list[i]
        key = member[0]
        value = member[1]
        ret += f'"{key}": '

        if isinstance(value, bytes):
            ret += f'"{value.hex()}"'
        else:
            ret += json.dumps(value)

        if i == length - 1:
            ret += "\n"
        else:
            ret += ",\n"

    ret += "}\n"
    return ret


def get_func_globals(func: types.FunctionType) -> dict:
    func_globs = func.__globals__
    needed_globs = func.__code__.co_names
    ret_globs = {}

    for glob in needed_globs:
        if glob in func_globs:
            ret_globs[glob] = func_globs[glob]

    return ret_globs


def dump_function(func) -> str:
    ret_str = str()
    ret_str += '{\n'
    ret_str += '"py/function": '
    ret_str += '"' + func.__module__ + "." + func.__name__ + '"'

    all_members = inspect.getmembers(func.__code__)
    member_list = list(filter(lambda member: member[0].startswith("co_"), all_members))

    ret_str += ",\n"

    func_globs = get_func_globals(func)
    ret_str += '"__globals__": '

    for glob_name in func_globs:
        if isinstance(func_globs[glob_name], types.ModuleType):
            func_globs[glob_name] = "__module_name__"

    ret_str += json.dumps(func_globs)
    ret_str += ",\n"

    ret_str += '"__code__": \n'
    ret_str += dump_func_code_info(member_list)

    ret_str += '}\n'
    return ret_str
"""
