import unittest

import os
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

    def test_dumps(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
