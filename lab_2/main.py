from json_serializer import JSONSerializer

import jsonpickle

class MyClass:
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3

    def show_info(self):
        print("x = " + str(self.x))
        print("y = " + str(self.y))
        print("z = " + str(self.z))


def hello_world():
    print("hello world")


def print_class_for_class_func_and_object():
    print(MyClass.__class__)
    print(MyClass().__class__)
    print(hello_world.__class__)


def print_docs_for_class_object():
    o = MyClass()
    print(o.__class__.__module__)
    print(o.__class__.__name__)


def print_class_members():
    o = MyClass
    # print(o.__dict__)
    method_list = [method for method in dir(o) if method.startswith('__') is False]

    for mtd in method_list:
        print(mtd)


def main():
    """
    print_class_for_class_func_and_object()
    print()
    print_docs_for_class_object()

    print_class_members()
    """
    encoded = jsonpickle.encode(hello_world)
    print(jsonpickle.encode(hello_world))
    jsonpickle.decode(encoded)()

    print("\n\n\n\n------------------------------------\n\n\n\n\n")

    a = JSONSerializer()
    # encoded = a.dumps(MyClass)
    encoded = a.dumps(hello_world)
    print("Encoded object string: " + encoded)

    decoded = a.loads(encoded)

    print("Decoded object: ")
    print("type: " + str(type(decoded)))
    print("object: " + str(decoded))


if __name__ == '__main__':
    main()
