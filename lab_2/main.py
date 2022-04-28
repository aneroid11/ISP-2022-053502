import inspect
import json
import math
from json_serializer import JSONSerializer
import converter
from pprint import pprint


c = 42


def hello_world():
    print("start hello_world()")

    a = {"a": 3, "b": 2}
    serialized_a = json.dumps(a)
    print(serialized_a)
    print(math.sin(c))

    print("end hello_world()")


def main_test_function(x):
    a = 123
    return math.sin(x * a * c)


def test_func_converting():
    func_info_dict = converter.prepare_func(hello_world)
    func_str = json.dumps(func_info_dict, indent=2)
    print(func_str)
    converter.load_func_from_info_dict(func_info_dict)()


class SimpleClass:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    """def some_method(self):
        print("hello world" + str(self.x))"""


def test_simple_object_converting():
    simple = SimpleClass(3, 4, 5)
    encoded = converter.prepare_object(simple)
    print("encoded object: ")
    print(encoded)

    decoded = converter.load_object_from_info_dict(encoded)
    print("decoded object:")
    print(decoded)


def main():
    """serializer = JSONSerializer()
    encoded = serializer.dumps(hello_world)
    print("Encoded object string:\n" + encoded)
    out_file = open("serialized_object.json", "w")
    serializer.dump(hello_world, out_file)
    out_file.close()"""
    test_simple_object_converting()


if __name__ == '__main__':
    main()
