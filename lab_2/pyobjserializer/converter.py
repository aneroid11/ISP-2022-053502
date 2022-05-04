import inspect
import types
import typing


def object_of_elementary_type(obj) -> bool:
    is_elem = (
        isinstance(obj, dict)
        or isinstance(obj, list)
        or isinstance(obj, str)
        or isinstance(obj, int)
        or isinstance(obj, float)
        or isinstance(obj, bool)
        or isinstance(obj, tuple)
        or obj is None
    )
    return is_elem


def prepare_class(cls: object) -> dict:
    # info_dict = {"py/type": cls.__module__ + "." + cls.__name__, "members": {}}
    info_dict = {"py/type": cls.__name__, "members": {}}

    cls_dict = dict(cls.__dict__)

    for member_name in cls_dict:
        value = cls_dict[member_name]
        value_typename = type(value).__name__

        if object_of_elementary_type(value):
            cls_dict[member_name] = value
        elif value_typename == "getset_descriptor":
            # skip
            continue
        elif value_typename == "function":
            # it is a function
            cls_dict[member_name] = prepare_func(value)
        elif value_typename == "method":
            # it is a method
            cls_dict[member_name] = prepare_func(value.__func__)
        elif value_typename == "type":
            # it is a global class
            cls_dict[member_name] = prepare_class(value)
        else:
            # it is an object
            cls_dict[member_name] = prepare_object(value)

        info_dict["members"][member_name] = cls_dict[member_name]

    return info_dict


def load_class_from_info_dict(info_dict: dict, globs: dict) -> object:
    name = info_dict["py/type"]
    members = info_dict["members"]

    for mem_name in members:
        current_member = members[mem_name]

        # load nested objects
        if isinstance(current_member, dict):
            if "py/object" in current_member:
                # it is an object
                # load this object recursively
                current_member = load_object_from_info_dict(current_member, globs)
            elif "py/function" in current_member:
                # it is a function
                current_member = load_func_from_info_dict(current_member, globs)

        members[mem_name] = current_member

    ret_class = type(name, (object,), members)

    return ret_class


def prepare_object(obj: object) -> dict:
    obj_info_dict = {"py/object": obj.__module__ + "." + type(obj).__name__}

    all_members = inspect.getmembers(obj)
    member_list = list(
        filter(lambda member: not member[0].startswith("__"), all_members)
    )

    member_dict = {}

    for mem in member_list:
        value = mem[1]

        if object_of_elementary_type(value):
            member_dict[mem[0]] = value
        elif type(value).__name__ == "method":
            # it is a method of the object
            member_dict[mem[0]] = prepare_func(value.__func__)
            pass
        else:
            # it is an object
            member_dict[mem[0]] = prepare_object(value)

    obj_info_dict["members"] = member_dict
    return obj_info_dict


class Empty:
    pass


def load_object_from_info_dict(info_dict: dict, globs: dict) -> object:
    members = info_dict["members"]
    ret_object = Empty()

    for mem_name in members:
        current_member = members[mem_name]

        # load nested objects
        if isinstance(current_member, dict) and "py/object" in current_member:
            # it is an object
            # load this object recursively
            current_member = load_object_from_info_dict(current_member, globs)
        if isinstance(current_member, dict) and "py/function" in current_member:
            # it is a method
            member_func = load_func_from_info_dict(current_member, globs)
            current_member = types.MethodType(member_func, ret_object)

        ret_object.__setattr__(mem_name, current_member)

    return ret_object


def prepare_func(func) -> dict:
    func_info_dict = {"py/function": func.__module__ + "." + func.__name__}

    func_globs = get_func_globals(func)
    for glob_name in func_globs:
        if isinstance(func_globs[glob_name], types.ModuleType):
            # it is a module
            func_globs[glob_name] = "__module_name__"
        elif isinstance(func_globs[glob_name], types.BuiltinFunctionType):
            # it is a built-in function
            func_globs[glob_name] = prepare_builtin_func(func_globs[glob_name])
        elif isinstance(func_globs[glob_name], types.FunctionType):
            # it is an ordinary function
            func_globs[glob_name] = prepare_func(func_globs[glob_name])
        elif type(func_globs[glob_name]).__name__ == "type":
            # it is a class
            func_globs[glob_name] = prepare_class(func_globs[glob_name])

    func_info_dict["__globals__"] = func_globs

    all_members = inspect.getmembers(func.__code__)
    member_list = list(filter(lambda member: member[0].startswith("co_"), all_members))
    func_info_dict["__code__"] = get_func_code_info(member_list)

    return func_info_dict


def prepare_builtin_func(builtin_func: object) -> dict:
    func_name = builtin_func.__name__
    module_name = builtin_func.__self__.__name__
    func_info_dict = {"py/builtin_function": func_name, "module": module_name}
    return func_info_dict


def load_builtin_func_from_info_dict(info_dict: dict) -> types.BuiltinFunctionType:
    loaded_func = __import__(info_dict["module"]).__getattribute__(
        info_dict["py/builtin_function"]
    )
    return loaded_func


def get_func_globals(func: types.FunctionType) -> dict:
    func_globs = func.__globals__
    needed_globs = func.__code__.co_names
    ret_globs = {}

    for glob in needed_globs:
        if glob in func_globs:
            ret_globs[glob] = func_globs[glob]

    return ret_globs


def get_func_code_info(member_list: list) -> dict:
    code_info = {}
    length = len(member_list)

    for i in range(0, length):
        member = member_list[i]
        key = member[0]
        value = member[1]

        if isinstance(value, bytes):
            value = value.hex()
        # all tuples must be transformed into lists here
        elif isinstance(value, tuple):
            value = tuple_to_list_recursive(value)

        code_info[key] = value

    return code_info


def load_func_from_info_dict(info_dict: dict, globs: dict) -> types.FunctionType:
    func_info = {}
    keys = info_dict["__code__"].keys()
    func_info["py/function"] = info_dict["py/function"]
    func_info["__code__"] = {}

    for key in keys:
        if key == "co_code" or key == "co_lnotab":
            value = bytes.fromhex(info_dict["__code__"][key])
        else:
            value = info_dict["__code__"][key]

        # all lists must be transformed into tuples here
        if isinstance(value, list):
            value = list_to_tuple_recursive(value)

        func_info["__code__"][key] = value

    func_code = types.CodeType(
        func_info["__code__"]["co_argcount"],
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
        func_info["__code__"]["co_cellvars"],
    )

    func_globs, updatable_globs_names = load_func_globals(info_dict, globs)
    func = types.FunctionType(func_code, func_globs)

    # to get the global values overriding those that were saved
    if globs is not None:
        for glob_name in updatable_globs_names:
            func.__globals__.update({glob_name: globs[glob_name]})

    return func


def load_func_globals(info: dict, globs: dict) -> typing.Tuple[dict, list]:
    if "__globals__" not in info:
        return globals().copy(), []

    ret_globs = globals().copy()
    additional_globs = info["__globals__"]
    updatable_globs_names = []

    for glob_name in additional_globs:
        curr_glob = additional_globs[glob_name]

        if isinstance(curr_glob, str) and curr_glob == "__module_name__":
            # glob_name is the name for a module
            additional_globs[glob_name] = __import__(glob_name)
        elif isinstance(curr_glob, dict) and "py/builtin_function" in curr_glob:
            # it is a built-in function
            additional_globs[glob_name] = load_builtin_func_from_info_dict(curr_glob)
        elif isinstance(curr_glob, dict) and "py/function" in curr_glob:
            # it is an ordinary function
            additional_globs[glob_name] = load_func_from_info_dict(curr_glob, globs)
        elif isinstance(curr_glob, dict) and "py/type" in curr_glob:
            # it is a class
            additional_globs[glob_name] = load_class_from_info_dict(curr_glob, globs)
        else:
            updatable_globs_names.append(glob_name)

    for glob_name in additional_globs:
        ret_globs[glob_name] = additional_globs[glob_name]

    return ret_globs, updatable_globs_names


def tuple_to_list_recursive(tpl: tuple) -> list:
    size = len(tpl)
    ret_list = list(tpl)

    for i in range(size):
        if isinstance(tpl[i], tuple):
            ret_list[i] = tuple_to_list_recursive(tpl[i])

    return ret_list


def list_to_tuple_recursive(lst: list) -> tuple:
    size = len(lst)

    for i in range(size):
        if isinstance(lst[i], list):
            lst[i] = list_to_tuple_recursive(lst[i])

    return tuple(lst)