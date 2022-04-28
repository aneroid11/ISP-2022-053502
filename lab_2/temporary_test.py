from json_serializer import JSONSerializer
import inspect


def test_loading_object():
    serializer = JSONSerializer()
    file = open("serialized_object.json", "r")
    loaded_obj = serializer.load(file)
    file.close()

    if inspect.isfunction(loaded_obj):
        print("it is a function!")
        loaded_obj()
    else:
        print("it is something else!")
        print(loaded_obj)
        print(loaded_obj.__dict__)
        print(loaded_obj.simple_obj.y)
        loaded_obj.print_sum()


if __name__ == "__main__":
    test_loading_object()
