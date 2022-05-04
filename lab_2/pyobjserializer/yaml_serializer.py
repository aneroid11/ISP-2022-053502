from .abstract_serializer import (
    AbstractSerializer,
    dumps_using_dumps_elementary,
    loads_using_loads_elementary,
)
import yaml


def yaml_dumps_elementary(elem_obj: object):
    return yaml.dump(elem_obj, indent=2)


def yaml_loads_elementary(elem_str: str) -> object:
    return yaml.safe_load(elem_str)


class YAMLSerializer(AbstractSerializer):
    def dumps(self, obj: object) -> str:
        return dumps_using_dumps_elementary(obj, yaml_dumps_elementary)

    def loads(self, string: str, globs: dict = None) -> object:
        return loads_using_loads_elementary(string, yaml_loads_elementary, globs)
