from .abstract_serializer import AbstractSerializer
from .json_serializer import JSONSerializer
from .toml_serializer import TOMLSerializer
from .yaml_serializer import YAMLSerializer


def create_serializer(format_name: str) -> AbstractSerializer:
    serializer_types = {
        "json": JSONSerializer,
        "yaml": YAMLSerializer,
        "toml": TOMLSerializer,
    }
    if format_name in serializer_types:
        return serializer_types[format_name]()
    raise NotImplementedError()
