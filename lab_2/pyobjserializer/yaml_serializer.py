"""The module that defines the YAMLSerializer class."""

import yaml

from .abstract_serializer import (AbstractSerializer,
                                  dumps_using_dumps_elementary,
                                  loads_using_loads_elementary)


def yaml_dumps_elementary(elem_obj: object):
    """Serialize an elementary object to YAML."""
    return yaml.dump(elem_obj, indent=2)


def yaml_loads_elementary(elem_str: str) -> object:
    """Construct an elementary object from a YAML string."""
    return yaml.safe_load(elem_str)


class YAMLSerializer(AbstractSerializer):
    """The class that implements AbstractSerializer for YAML."""

    def dumps(self, obj: object) -> str:
        """Serialize obj to a YAML string."""
        return dumps_using_dumps_elementary(obj, yaml_dumps_elementary)

    def loads(self, string: str, globs: dict = None) -> object:
        """Deserialize string to an object. Optionally update the object globals using globs."""
        return loads_using_loads_elementary(string, yaml_loads_elementary, globs)
