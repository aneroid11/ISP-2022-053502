from create_serializer import create_serializer


c = 553


def load_object(serializer_name: str) -> object:
    serializer = create_serializer(serializer_name)

    with open("test_serialized_object." + serializer_name, "r") as file:
        ret_object = serializer.load(file, globals())

    return ret_object
