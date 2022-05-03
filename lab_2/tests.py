import unittest
import os
import my_json
import json
import abstract_serializer
from json_serializer import JSONSerializer
from yaml_serializer import YAMLSerializer
from toml_serializer import TOMLSerializer
from create_serializer import create_serializer


class TestCreateSerializer(unittest.TestCase):
    def test_create_serializer(self):
        serializer = create_serializer("json")
        self.assertTrue(type(serializer) == JSONSerializer)
        serializer = create_serializer("yaml")
        self.assertTrue(type(serializer) == YAMLSerializer)
        serializer = create_serializer("toml")
        self.assertTrue(type(serializer) == TOMLSerializer)

        with self.assertRaises(NotImplementedError):
            create_serializer("oadkoaskdo")


class TestAbstractSerializer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serializer = abstract_serializer.AbstractSerializer()

    @classmethod
    def tearDownClass(cls):
        os.remove("dumped.txt")

    def test_dumps(self):
        obj = {"a": "a", "b": "b"}

        with self.assertRaises(NotImplementedError):
            self.serializer.dumps(3)

        with self.assertRaises(NotImplementedError), open("dumped.txt", "w") as file:
            self.serializer.dump(3, file)

    def test_loads(self):
        with self.assertRaises(NotImplementedError):
            self.serializer.loads("")

        with self.assertRaises(NotImplementedError), open("dumped.txt", "r") as file:
            self.serializer.load(file)


class TestJSONSerializerDumping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serializer = create_serializer("json")

    # def test_dumps(self):
    #    self.assertEqual(True, True)


class TestMyJSON(unittest.TestCase):
    def test_my_json(self):
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
                     (2, 3, None, True,
                      [(3,
                        # "hello,\\\" 'hehe''world",
                        "hello, 'hehe', world",
                        "k"), 4]),
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
            my_json_encoded = my_json.dumps(obj)
            json_encoded = json.dumps(obj)
            self.assertEqual(my_json_encoded, json_encoded)
            my_json_decoded = my_json.loads(my_json_encoded)
            json_decoded = json.loads(my_json_encoded)
            self.assertEqual(my_json_decoded, json_decoded)


if __name__ == "__main__":
    unittest.main()
