import json
import math
from json_serializer import JSONSerializer
import converter


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


def test_converter():
    func_info_dict = converter.prepare_func(hello_world)
    func_str = json.dumps(func_info_dict, indent=2)
    print(func_str)
    converter.load_func_from_info_dict(func_info_dict)()


def main():
    serializer = JSONSerializer()
    encoded = serializer.dumps(hello_world)
    print("Encoded object string:\n" + encoded)
    out_file = open("serialized_object.json", "w")
    serializer.dump(hello_world, out_file)
    out_file.close()


if __name__ == '__main__':
    main()
