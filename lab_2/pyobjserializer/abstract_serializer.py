from typing import TextIO
from . import converter


class AbstractSerializer:
    def dumps(self, obj: object) -> str:
        raise NotImplementedError()

    def dump(self, obj: object, fp: TextIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def loads(self, string: str, globs: dict = None) -> object:
        raise NotImplementedError()

    def load(self, fp: TextIO, globs: dict = None) -> object:
        data_string = str(fp.read())
        return self.loads(data_string, globs)


def dumps_using_dumps_elementary(obj: object,
                                 dumps_elementary) -> str:
    if converter.object_of_elementary_type(obj):
        dumped = dumps_elementary(obj)
    else:
        tp = str(obj.__class__)

        if tp == "<class 'type'>":
            dumped = dumps_elementary(converter.prepare_class(obj))
        elif tp == "<class 'function'>":
            dumped = dumps_elementary(converter.prepare_func(obj))
        elif tp == "<class 'builtin_function_or_method'>":
            dumped = dumps_elementary(converter.prepare_builtin_func(obj))
        else:
            # it is an object of some user class
            dumped = dumps_elementary(converter.prepare_object(obj))

    return dumped


def loads_using_loads_elementary(string: str,
                                 loads_elementary,
                                 globs: dict = None) -> object:
    decoded_object = loads_elementary(string)
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
