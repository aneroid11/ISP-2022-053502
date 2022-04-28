import inspect
import json
# import math
from math import sin
import types
from json_serializer import JSONSerializer
import converter
from pprint import pprint


c = 42


def hello_world():
    sin(2)

    print("start hello_world()")

    a = {"a": 3, "b": 2}
    serialized_a = json.dumps(a)
    print(serialized_a)
    # print(math.sin(c))
    # print(sin(c))

    print("end hello_world()")


def main_test_function(x):
    a = 123

    print("a ==", a)
    print("c ==", c)
    print("x ==", x)

    # return math.sin(x * a * c)
    return sin(x * a * c)


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


class NotSoSimpleClass:
    def __init__(self, x, y, z):
        self.simple_obj = SimpleClass(x, y, z)


class NotSoSimpleWithMethods:
    def __init__(self, x, y, z):
        self.some_property = None
        self.simple_obj = SimpleClass(x, y, z)

    def print_sum(self):
        # print(self.simple_obj.x + self.simple_obj.y + self.simple_obj.z)
        self.some_property = 3.14 / 2
        print("here we need to print the sum of x, y and z")
        print("sin(self.some_property) =", sin(self.some_property))
        hello_world()


def test_object_converting():
    obj = NotSoSimpleWithMethods(3, 4, 5)
    encoded = converter.prepare_object(obj)
    print("encoded object: ")
    # pprint(encoded)
    print(json.dumps(encoded, indent=2))

    decoded = converter.load_object_from_info_dict(encoded)
    print("\ndecoded object:")
    decoded.print_sum()


def main():
    test_object_converting()

    """serializer = JSONSerializer()
    obj = NotSoSimpleWithMethods(3, 4, 5)
    out_file = open("serialized_object.json", "w")
    serializer.dump(obj, out_file)
    out_file.close()"""


if __name__ == '__main__':
    main()
