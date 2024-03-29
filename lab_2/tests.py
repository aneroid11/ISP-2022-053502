"""Testing module for the pyobjserializer library."""

import json
import os
import unittest
from math import sin

import loading_tests
from pyobjserializer import abstract_serializer
from pyobjserializer.create_serializer import create_serializer
from pyobjserializer.json_serializer import JSONSerializer
from pyobjserializer.my_json import dumps, loads
from pyobjserializer.toml_serializer import TOMLSerializer
from pyobjserializer.yaml_serializer import YAMLSerializer


class TestCreateSerializer(unittest.TestCase):
    """Testing the create_serializer() function."""

    def test_create_serializer(self):
        """Test that create_serializer() creates serializers of valid type."""
        serializer = create_serializer("json")
        self.assertTrue(type(serializer) == JSONSerializer)
        serializer = create_serializer("yaml")
        self.assertTrue(type(serializer) == YAMLSerializer)
        serializer = create_serializer("toml")
        self.assertTrue(type(serializer) == TOMLSerializer)

        with self.assertRaises(NotImplementedError):
            create_serializer("oadkoaskdo")


class TestAbstractSerializer(unittest.TestCase):
    """Test the AbstractSerializer class."""

    @classmethod
    def setUpClass(cls):
        """Create a serializer to test."""
        cls.serializer = abstract_serializer.AbstractSerializer()

    @classmethod
    def tearDownClass(cls):
        """Delete used files."""
        os.remove("dumped.txt")

    def test_dumps(self):
        """Check that AbstractSerializer cannot dump objects."""
        obj = {"a": "a", "b": "b"}

        with self.assertRaises(NotImplementedError):
            self.serializer.dumps(obj)

        with self.assertRaises(NotImplementedError), open("dumped.txt", "w") as file:
            self.serializer.dump(obj, file)

    def test_loads(self):
        """Check that AbstractSerializer cannot load objects."""
        with self.assertRaises(NotImplementedError):
            self.serializer.loads("")

        with self.assertRaises(NotImplementedError), open("dumped.txt", "r") as file:
            self.serializer.load(file)


c = 42


def main_test_function(x):
    """Do some test actions. Use a global variable and an imported function."""
    a = 123

    return sin(x * a * c)


class SimpleClass:
    """A simple class to serialize."""

    def __init__(self, x, y, z):
        """Create some simple members."""
        self.x = x
        self.y = y
        self.z = z


class NotSoSimpleWithMethods:
    """A complex class to serialize. Contains methods, variables and references to global functions and classes."""

    prop_1 = 66
    prop_2 = 77
    prop_3 = 88
    prop_4 = 99
    attr_1 = SimpleClass(0, 0, 0)

    def __init__(self, x, y, z):
        """Initialize class instance with some basic values."""
        self.some_property = None
        self.simple_obj = SimpleClass(x, y, z)

    def some_method(self) -> float:
        """Do some action that uses a flobal function."""
        self.some_property = 3.14 / 2
        return main_test_function(self.some_property)


class TestSerializers(unittest.TestCase):
    """A class to check if serializers are working properly."""

    def test_dump_load_objects(self):
        """Dump test objects, load them and compare initial version with the decoded."""
        serializer_names = ["json", "yaml", "toml"]

        objects_with_check_methods = [
            (NotSoSimpleWithMethods, self.check_decoded_class),
            ({"a": 323, "b": 235234}, self.check_decoded_elementary_object),
            (main_test_function, self.check_decoded_func),
            (sin, self.check_decoded_builtin_func),
            (NotSoSimpleWithMethods(1, 2, 3), self.check_decoded_object),
            ("encoded string", self.check_decoded_string),
        ]

        for obj_with_check in objects_with_check_methods:
            for name in serializer_names:
                serializer = create_serializer(name)

                obj = obj_with_check[0]
                check = obj_with_check[1]

                with open("test_serialized_object." + name, "w") as file_output:
                    serializer.dump(obj, file_output)

                decoded = loading_tests.load_object(name)
                os.remove("test_serialized_object." + name)
                check(decoded)

    def check_decoded_class(self, decoded):
        """Check if decoded matches the NotSoSimpleWithMethods class."""
        self.assertEqual(decoded.prop_1, 66)
        self.assertEqual(decoded.prop_2, 77)
        self.assertEqual(decoded.prop_3, 88)
        self.assertEqual(decoded.prop_4, 99)
        self.assertEqual(decoded.attr_1.x, 0)
        self.assertEqual(decoded.attr_1.y, 0)
        self.assertEqual(decoded.attr_1.z, 0)
        decoded_obj = decoded(1, 2, 3)
        self.assertEqual(decoded_obj.some_property, None)
        self.assertEqual(decoded_obj.simple_obj.x, 1)
        self.assertEqual(decoded_obj.simple_obj.y, 2)
        self.assertEqual(decoded_obj.simple_obj.z, 3)
        self.assertEqual(decoded_obj.some_method(), sin(3.14 / 2 * 123 * 553))

    def check_decoded_elementary_object(self, decoded):
        """Check if decoded matches the dictionary."""
        self.assertEqual(decoded, {"a": 323, "b": 235234})

    def check_decoded_string(self, decoded):
        """Check if decoded matches an example string."""
        self.assertEqual(decoded, "encoded string")

    def check_decoded_func(self, decoded):
        """Check if decoded matches main_test_function()."""
        self.assertEqual(decoded(132), sin(132 * 123 * 553))

    def check_decoded_builtin_func(self, decoded):
        """Check if decoded matches sin()."""
        self.assertEqual(decoded(3.14), sin(3.14))

    def check_decoded_object(self, decoded_obj):
        """Check if decoded_obj matches an instance of NotSoSimpleWithMethods."""
        self.assertEqual(decoded_obj.some_property, None)
        self.assertEqual(decoded_obj.simple_obj.x, 1)
        self.assertEqual(decoded_obj.simple_obj.y, 2)
        self.assertEqual(decoded_obj.simple_obj.z, 3)
        self.assertEqual(decoded_obj.some_method(), sin(3.14 / 2 * 123 * 553))


class TestMyJSON(unittest.TestCase):
    """Test the my_json.py module."""

    def test_my_json(self):
        """Dump, load and check an object containing everything that my_json should serialize."""
        test_list = [
            5,
            "jojo",
            None,
            "jojo_2",
            4.2131321,
            True,
            True,
            False,
            [1, 2, 3, True, [1, 2], 1],
            [1, 2, 3, 4, True, False],
            (
                2,
                3,
                None,
                True,
                [
                    (
                        3,
                        "hello, 'hehe', world",
                        "k",
                    ),
                    4,
                ],
            ),
            {
                "2": "hello: world",
                "3": [1, 2, 3, True, [1, 2], 1],
                "dd": [1, 2, 3, True, [1, 2], 1],
                "inside_dict": {"ins1": "i", "ins2": "j"},
                "empty_list": [],
                "empty_dict": {},
                "Nonenenen": None,
            },
        ]

        for obj in test_list:
            my_json_encoded = dumps(obj)
            json_encoded = json.dumps(obj)
            self.assertEqual(my_json_encoded, json_encoded)
            my_json_decoded = loads(my_json_encoded)
            json_decoded = json.loads(my_json_encoded)
            self.assertEqual(my_json_decoded, json_decoded)


if __name__ == "__main__":
    unittest.main()
