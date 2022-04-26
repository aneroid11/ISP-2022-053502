import json
import math
import dis
import dill
from json_serializer import JSONSerializer
import types


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


c = 42


def main_test_function(x):
    a = 123
    return math.sin(x * a * c)


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


def get_globals_to_save(func) -> dict:
    func_names = func.__code__.co_names
    func_globs = func.__globals__
    ret_globs = {}

    for name in func_names:
        if name in func_globs:
            ret_globs[name] = func_globs[name]

    return ret_globs


def test_function_creating():
    def y():
        print(math.sin(2 * math.pi))
        print("hello world")

    # name = "func_name"
    y_code = types.CodeType(y.__code__.co_argcount,
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
                            y.__code__.co_name,
                            y.__code__.co_firstlineno,
                            y.__code__.co_lnotab,
                            y.__code__.co_freevars,
                            y.__code__.co_cellvars)

    print(get_globals_to_save(y))

    # func = types.FunctionType(y_code, y.__globals__, name)
    # func = types.FunctionType(y_code, y.__globals__)
    # func = types.FunctionType(y_code, globals())
    globs = y.__globals__
    func = types.FunctionType(y_code, globs)
    # my_globals = dict()
    # func = types.FunctionType(y_code, my_globals)
    """print(func.__class__)
    print(func.__name__)
    print(func.__module__)"""
    # print(func.__module__)

    func()


def main():
    serializer = JSONSerializer()
    # encoded = a.dumps(MyClass)
    encoded = serializer.dumps(hello_world)
    print("Encoded object string:\n" + encoded)
    out_file = open("serialized_object.json", "w")
    serializer.dump(hello_world, out_file)
    out_file.close()

    """decoded = a.loads(encoded)

    print("Decoded object: ")
    print("type: " + str(type(decoded)))
    print("object: " + str(decoded))
    decoded()"""

    """test_function_creating()

    mth = math
    print(mth.sin(2*mth.pi))
    # mod = types.ModuleType("math")
    mod = __import__("math")
    print(mod.sin(2 * mod.pi))"""

    """keys = hello_world.__globals__.keys()

    print("\n__globals__\n")
    for key in keys:
        print(key + ":", hello_world.__globals__[key])
        print("the type of __globals__[key]:", type(hello_world.__globals__[key]))"""


if __name__ == '__main__':
    main()
