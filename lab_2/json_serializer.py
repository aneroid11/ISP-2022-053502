import typing
from typing import TextIO
from abstract_serializer import AbstractSerializer
import json
import inspect
import types


class JSONSerializer(AbstractSerializer):
    def dumps(self, obj: object) -> str:
        try:
            dumped = json.dumps(obj)
        except TypeError:
            # this is not a simple type. we need a title for the dict
            # if this is a class
            tp = str(obj.__class__)

            if tp == "<class 'type'>":
                dumped = dump_class(obj)
            elif tp == "<class 'function'>":
                dumped = dump_function(obj)
            else:
                dumped = dump_object(obj)

        return dumped

    def loads(self, string: str) -> object:
        decoded_object = json.loads(string)

        if isinstance(decoded_object, dict):
            if "py/function" in decoded_object:
                return load_function(decoded_object)

        return decoded_object

    def dump(self, obj: object, fp: TextIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def load(self, fp: TextIO) -> object:
        data_string = str(fp.read())
        return self.loads(data_string)


def get_class_name(cls: object) -> str:
    return cls.__module__ + '.' + cls.__name__


def dump_class(cls: object) -> str:
    ret_str = str()
    ret_str += '{'
    ret_str += '}'
    return ret_str


def dump_object(obj: object) -> str:
    ret_str = str()
    ret_str += '{'
    ret_str += '}'
    return ret_str


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
            print(key, ":", value)
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


def load_func_globals(info: dict) -> dict:
    if "__globals__" not in info:
        return globals()

    ret_globs = globals()
    additional_globs = info["__globals__"]

    for glob_name in additional_globs:
        curr_glob = additional_globs[glob_name]

        if isinstance(curr_glob, str) and curr_glob == "__module_name__":
            # glob_name is the name for a module
            additional_globs[glob_name] = __import__(glob_name)

    for glob_name in additional_globs:
        ret_globs[glob_name] = additional_globs[glob_name]

    return ret_globs


def list_to_tuple_recursive(lst: list) -> typing.Tuple:
    size = len(lst)

    for i in range(size):
        if isinstance(lst[i], list):
            lst[i] = list_to_tuple_recursive(lst[i])

    return tuple(lst)


def load_function(info: dict):
    func_info = {}
    keys = info["__code__"].keys()
    func_info["py/function"] = info["py/function"]
    func_info["__code__"] = {}

    for key in keys:
        if key == "co_code" or key == "co_lnotab":
            value = bytes.fromhex(info["__code__"][key])
        else:
            value = info["__code__"][key]

        # all lists must be transformed into tuples here
        if isinstance(value, list):
            # value = tuple(value)
            value = list_to_tuple_recursive(value)

        func_info["__code__"][key] = value

    func_code = types.CodeType(func_info["__code__"]["co_argcount"],
                               func_info["__code__"]["co_posonlyargcount"],
                               func_info["__code__"]["co_kwonlyargcount"],
                               func_info["__code__"]["co_nlocals"],
                               func_info["__code__"]["co_stacksize"],
                               func_info["__code__"]["co_flags"],
                               func_info["__code__"]["co_code"],
                               func_info["__code__"]["co_consts"],
                               func_info["__code__"]["co_names"],
                               func_info["__code__"]["co_varnames"],
                               func_info["__code__"]["co_filename"],
                               func_info["__code__"]["co_name"],
                               func_info["__code__"]["co_firstlineno"],
                               func_info["__code__"]["co_lnotab"],
                               func_info["__code__"]["co_freevars"],
                               func_info["__code__"]["co_cellvars"])

    func_globs = load_func_globals(info)
    """if "__globals__" in func_info.keys():
        # func_globs = globals()
        # do something
        additional_globs = func_info["__globals__"]
        keys = additional_globs.keys()

        for key in keys:
            func_globs[key] = additional_globs[key]"""

    func = types.FunctionType(func_code, func_globs)

    return func
