"""This module is needed for loading objects in an environment that differs from which they were dumped from."""

from pyobjserializer.create_serializer import create_serializer

c = 553


def load_object(serializer_name: str) -> object:
    """Load an object from test_serialized_object.[format_name] file."""
    serializer = create_serializer(serializer_name)

    with open("test_serialized_object." + serializer_name, "r") as file:
        ret_object = serializer.load(file, globals())

    return ret_object
