from create_serializer import create_serializer


c = 553


def load_object() -> object:
    serializer = create_serializer("json")

    with open("test_serialized_object.json", "r") as file:
        ret_object = serializer.load(file, globals())

    return ret_object
