from json_serializer import JSONSerializer


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


import types


def test_function_creating():
    def y():
        print("hello world")

    argcount = 0
    name = "func_name"
    y_code = types.CodeType(argcount,
                            y.__code__.co_posonlyargcount,
                            y.__code__.co_kwonlyargcount,
                            y.__code__.co_nlocals,
                            y.__code__.co_stacksize,
                            y.__code__.co_flags,
                            y.__code__.co_code,
                            y.__code__.co_consts,
                            y.__code__.co_names,
                            y.__code__.co_varnames,
                            y.__code__.co_filename,
                            name,
                            y.__code__.co_firstlineno,
                            y.__code__.co_lnotab,
                            y.__code__.co_freevars,
                            y.__code__.co_cellvars)

    func = types.FunctionType(y_code, y.__globals__, name)
    func()


def main():
    a = JSONSerializer()
    # encoded = a.dumps(MyClass)
    encoded = a.dumps(hello_world)
    print("Encoded object string:\n" + encoded)

    decoded = a.loads(encoded)

    """print("Decoded object: ")
    print("type: " + str(type(decoded)))
    print("object: " + str(decoded))
    decoded()"""
    # test_function_creating()


if __name__ == '__main__':
    main()
