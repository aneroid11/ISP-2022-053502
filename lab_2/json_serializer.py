from io import FileIO
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

    def dump(self, obj: object, fp: FileIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def load(self, fp: FileIO) -> object:
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
            ret += json.dumps(value)

        if i == length - 1:
            ret += "\n"
        else:
            ret += ",\n"

    ret += "}\n"
    return ret


def dump_function(func) -> str:
    ret_str = str()
    ret_str += '{\n'
    ret_str += '"py/function": '
    ret_str += '"' + func.__module__ + "." + func.__name__ + '"'

    all_members = inspect.getmembers(func.__code__)
    member_list = list(filter(lambda member: member[0].startswith("co_"), all_members))

    ret_str += ",\n"

    """
    ret_str += '"__globals__": \n'
    ret_str += "{\n"
    ret_str += "},\n"
    """

    ret_str += '"code_info": \n'
    ret_str += dump_func_code_info(member_list)

    ret_str += '}\n'
    return ret_str


def load_function(info: dict):
    # to start with - just co_code
    func_info = {}
    keys = info["code_info"].keys()
    func_info["py/function"] = info["py/function"]
    func_info["code_info"] = {}

    for key in keys:
        value = bytes.fromhex(info["code_info"][key]) if key == "co_code" else info["code_info"][key]
        func_info["code_info"][key] = value

    def do_something():
        print(func_info)

    return do_something
