"""The module that defines the JSONSerializer class."""

from . import my_json as json
from .abstract_serializer import (AbstractSerializer,
                                  dumps_using_dumps_elementary,
                                  loads_using_loads_elementary)


def json_dumps_elementary(elem_obj: object):
    """Dump en elementary object to json."""
    return json.dumps(elem_obj)


def json_loads_elementary(elem_str: str) -> object:
    """Load an elementary object from json."""
    return json.loads(elem_str)


class JSONSerializer(AbstractSerializer):
    """A class implementing AbstractSerializer for JSON."""

    def dumps(self, obj: object) -> str:
        """Dump obj to a JSON string."""
        return dumps_using_dumps_elementary(obj, json_dumps_elementary)

    def loads(self, string: str, globs: dict = None) -> object:
        """Load an object from a JSON string. Optionally update object globals using globs."""
        return loads_using_loads_elementary(string, json_loads_elementary, globs)
