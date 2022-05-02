import json
from math import sin
from json_serializer import JSONSerializer
import converter
import temporary_test


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
    prop_1 = 66
    prop_2 = 77
    prop_3 = 88
    prop_4 = 99
    attr_1 = SimpleClass(0, 0, 0)

    def __init__(self, x, y, z):
        self.some_property = None
        self.simple_obj = SimpleClass(x, y, z)

    def __hash__(self):
        return 1

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
    # print(json.dumps(encoded, indent=2))

    decoded = converter.load_object_from_info_dict(encoded)
    print("\ndecoded object:")
    decoded.print_sum()


def test_class_converting():
    # pprint(dict(cls.__dict__))

    cls = NotSoSimpleWithMethods
    encoded = converter.prepare_class(cls)
    print("encoded class: ")
    # pprint(encoded)
    print(json.dumps(encoded, indent=2))

    decoded = converter.load_class_from_info_dict(encoded)

    print("\ndecoded object:")
    print(decoded)
    # obj = decoded(1, 2, 3)
    obj = decoded(5, 6, 7)
    print(obj.print_sum)
    obj.print_sum()


def hello_world_method(self):
    print("hello world method")


def test_create_class_dynamically():
    my_class = type("SomeClass",
                    (object, ),
                    {
                        "hello_world": hello_world_method
                    })
    my_class_object = my_class()
    my_class_object.hello_world()


def main():
    # test_class_converting()

    serializer = JSONSerializer()
    obj = NotSoSimpleWithMethods
    """out_file = open("serialized_object.json", "w")
    serializer.dump(obj, out_file)
    out_file.close()"""

    encoded = serializer.dumps(obj)
    print("encoded obj:")
    print(encoded)
    temporary_test.test_loading_object(encoded)


if __name__ == '__main__':
    main()
