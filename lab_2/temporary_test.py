from json_serializer import JSONSerializer
import inspect


def test_loading_function():
    serializer = JSONSerializer()
    file = open("serialized_object.json", "r")
    loaded_func = serializer.load(file)
    file.close()

    if inspect.isfunction(loaded_func):
        print("it is a function!")
        loaded_func()


if __name__ == "__main__":
    test_loading_function()
