from create_serializer import create_serializer
# import inspect


c = 553


def load_object() -> object:
    serializer = create_serializer("json")

    with open("serialized_object.json", "r") as file:
        ret_object = serializer.load(file, globals())

    return ret_object

    """if serialized_str is None:
        file = open("serialized_object.json", "r")
        loaded_obj = serializer.load(file)
        file.close()
    else:
        loaded_obj = serializer.loads(serialized_str, globals())

    if inspect.isfunction(loaded_obj):
        print("it is a function!")
        print(loaded_obj(1))
        # loaded_obj()
    elif inspect.isclass(loaded_obj):
        print("it is a class!")
        print(loaded_obj)
        new_obj = loaded_obj(8, 9, 10)
        new_obj.print_sum()
        print(new_obj.simple_obj.x)
        print(new_obj.simple_obj.y)
        print(new_obj.simple_obj.z)
    else:
        print("it is something else!")
        print(loaded_obj)
        # print(loaded_obj.simple_obj.y)
        # loaded_obj.print_sum()"""
