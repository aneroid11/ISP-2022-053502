from json_serializer import JSONSerializer
from yaml_serializer import YAMLSerializer
import inspect


c = 553


def test_loading_object(serialized_str=None):
    # serializer = JSONSerializer()
    serializer = YAMLSerializer()

    if serialized_str is None:
        file = open("serialized_object.json", "r")
        loaded_obj = serializer.load(file)
        file.close()
    else:
        loaded_obj = serializer.loads(serialized_str, globals())

    if inspect.isfunction(loaded_obj):
        print("it is a function!")
        # loaded_obj.__globals__.update({"c": globals()["c"]})
        # print(loaded_obj(1))
        loaded_obj()
    elif inspect.isclass(loaded_obj):
        print("it is a class!")
        print(loaded_obj)
        new_obj = loaded_obj(8, 9, 10)
        new_obj.print_sum()
    else:
        print("it is something else!")
        print(loaded_obj.simple_obj.y)
        loaded_obj.print_sum()


if __name__ == "__main__":
    test_loading_object()
