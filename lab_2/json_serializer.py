from typing import TextIO
from abstract_serializer import AbstractSerializer
from converter import prepare_func, load_func_from_info_dict
import json


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
                dumped = json.dumps(prepare_func(obj), indent=2)
            else:
                dumped = dump_object(obj)

        return dumped

    def loads(self, string: str) -> object:
        decoded_object = json.loads(string)

        if isinstance(decoded_object, dict):
            if "py/function" in decoded_object:
                return load_func_from_info_dict(decoded_object)

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
