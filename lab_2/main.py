from math import sin
import my_json
from create_serializer import create_serializer
import loading_tests


def test_my_json():
    test_list = [5,
                 "jojo",
                 None,
                 "jojo_2",
                 4.2131321,
                 True,
                 True,
                 False,
                 [1, 2, 3, True, [1, 2], 1],
                 [1, 2, 3, 4, True, False],
                 (2, 3, None, True, [(3, "hello,\\ \" 'hehe''world", "k"), 4]),
                 {
                     '2': "hello: world",
                     '3': [1, 2, 3, True, [1, 2], 1],
                     "dd": [1, 2, 3, True, [1, 2], 1],
                     "inside_dict": {"ins1": "i", "ins2": "j"},
                     "empty_list": [],
                     "empty_dict": {},
                     "Nonenenen": None
                 }]

    for obj in test_list:
        print("object:")
        print(obj)
        print("encoded object:")
        encoded = my_json.dumps(obj)
        print(encoded)
        print("decoded object:")
        decoded = my_json.loads(encoded)
        print(decoded)


def main():
    # test_my_json()
    # print(["\\, \""])

    serializer = create_serializer("json")
    # obj = NotSoSimpleWithMethods
    obj = 191230
    out_file = open("serialized_object.json", "w")
    serializer.dump(obj, out_file)
    out_file.close()

    encoded = serializer.dumps(obj)
    print("encoded obj:")
    print(encoded)
    # loading_tests.test_loading_object(encoded)


if __name__ == '__main__':
    main()
