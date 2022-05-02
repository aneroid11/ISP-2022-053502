from typing import TextIO
from abstract_serializer import AbstractSerializer
import converter
import json


class JSONSerializer(AbstractSerializer):
    def dumps(self, obj: object) -> str:
        if converter.object_of_elementary_type(obj):
            dumped = json.dumps(obj, indent=2)
        else:
            tp = str(obj.__class__)

            if tp == "<class 'type'>":
                dumped = json.dumps(converter.prepare_class(obj), indent=2)
            elif tp == "<class 'function'>":
                dumped = json.dumps(converter.prepare_func(obj), indent=2)
            else:
                dumped = json.dumps(converter.prepare_object(obj), indent=2)

        return dumped

    def dump(self, obj: object, fp: TextIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def loads(self, string: str, globs: dict = None) -> object:
        decoded_object = json.loads(string)
        globs_passed = None if globs is None else globs.copy()

        if isinstance(decoded_object, dict):
            if "py/function" in decoded_object:
                return converter.load_func_from_info_dict(decoded_object, globs_passed)
            elif "py/builtin_function" in decoded_object:
                return converter.load_builtin_func_from_info_dict(decoded_object)
            elif "py/type" in decoded_object:
                return converter.load_class_from_info_dict(decoded_object, globs_passed)
            elif "py/object" in decoded_object:
                return converter.load_object_from_info_dict(decoded_object, globs_passed)

        return decoded_object

    def load(self, fp: TextIO, globs: dict = None) -> object:
        data_string = str(fp.read())
        return self.loads(data_string, globs)
