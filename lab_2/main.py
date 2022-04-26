import json
import math
from json_serializer import JSONSerializer


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


def main():
    serializer = JSONSerializer()
    encoded = serializer.dumps(main_test_function)
    print("Encoded object string:\n" + encoded)
    out_file = open("serialized_object.json", "w")
    serializer.dump(main_test_function, out_file)
    out_file.close()


if __name__ == '__main__':
    main()
