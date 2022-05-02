from typing import TextIO
from abstract_serializer import AbstractSerializer
import converter
import json


class JSONSerializer(AbstractSerializer):
    def dumps(self, obj: object) -> str:
        try:
            dumped = json.dumps(obj)
        except TypeError:
            tp = str(obj.__class__)

            if tp == "<class 'type'>":
                dumped = json.dumps(converter.prepare_class(obj), indent=2)
            elif tp == "<class 'function'>":
                dumped = json.dumps(converter.prepare_func(obj), indent=2)
            else:
                dumped = json.dumps(converter.prepare_object(obj), indent=2)

        return dumped

    def loads(self, string: str) -> object:
        decoded_object = json.loads(string)

        if isinstance(decoded_object, dict):
            if "py/function" in decoded_object:
                return converter.load_func_from_info_dict(decoded_object)
            elif "py/type" in decoded_object:
                return converter.load_class_from_info_dict(decoded_object)
            elif "py/object" in decoded_object:
                return converter.load_object_from_info_dict(decoded_object)

        return decoded_object

    def dump(self, obj: object, fp: TextIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def load(self, fp: TextIO) -> object:
        data_string = str(fp.read())
        return self.loads(data_string)
