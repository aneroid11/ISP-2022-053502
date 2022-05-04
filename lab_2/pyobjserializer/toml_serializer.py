"""The module that defines the TOMLSerializer class."""

import tomli
import tomli_w

from .abstract_serializer import (AbstractSerializer,
                                  dumps_using_dumps_elementary,
                                  loads_using_loads_elementary)


def none_converter_recursive(obj: object, match: object):
    """
    Replace all Nones found in obj with '__None__' (and vice versa).

    This is necessary because TOML does not have any None type.
    """
    if match is obj is None:
        return "__None__"
    if obj == match == "__None__":
        return None

    if isinstance(obj, dict):
        keys = obj.keys()
        for key in keys:
            obj[key] = none_converter_recursive(obj[key], match)
        return obj
    if isinstance(obj, list):
        size = len(obj)
        for i in range(size):
            obj[i] = none_converter_recursive(obj[i], match)
        return obj
    return obj


def toml_dumps_elementary(elem_obj: object):
    """Serialize an elementary object to TOML."""
    if not isinstance(elem_obj, dict):
        # convert to dict
        elem_obj = {"py/elem_obj_not_dict": elem_obj}

    # replace all Nones with "__None__" strings
    elem_obj = none_converter_recursive(elem_obj, None)
    if not isinstance(elem_obj, dict):
        raise TypeError()

    return tomli_w.dumps(elem_obj)


def toml_loads_elementary(elem_str: str) -> object:
    """Construct an elementary object from a TOML string."""
    loaded = tomli.loads(elem_str)

    if "py/elem_obj_not_dict" in loaded:
        loaded = loaded["py/elem_obj_not_dict"]
    # replace all "__None__" strings with Nones
    return none_converter_recursive(loaded, "__None__")


class TOMLSerializer(AbstractSerializer):
    """The class that implements AbstractSerializer for TOML."""

    def dumps(self, obj: object) -> str:
        """Serialize obj to a TOML string."""
        return dumps_using_dumps_elementary(obj, toml_dumps_elementary)

    def loads(self, string: str, globs: dict = None) -> object:
        """Deserialize string to an object. Optionally update the object globals using globs."""
        return loads_using_loads_elementary(string, toml_loads_elementary, globs)
