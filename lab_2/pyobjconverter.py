#!/usr/bin/python3
"""
A console utility to convert Python objects from one format to another.

Supported formats: JSON, YAML, TOML.
"""

from argparse import ArgumentParser
from configparser import ConfigParser
from sys import exit

from pyobjserializer.create_serializer import create_serializer


def convert_file(input_file_name: str, initial_format: str, output_format: str):
    """Convert a serialized Python object from initial_format to output_format."""
    if initial_format == output_format:
        return None

    output_file_name = input_file_name + "." + output_format
    input_file_name += "." + initial_format

    try:
        input_serializer = create_serializer(initial_format)
        output_serializer = create_serializer(output_format)
    except NotImplementedError:
        print("no serializer for", initial_format, "or", output_format)
        exit(1)

    with open(input_file_name, "r") as file:
        obj = input_serializer.load(file)

    with open(output_file_name, "w") as file:
        output_serializer.dump(obj, file)


def main():
    """Entry point for the utility."""
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="input file (without the extension)")
    parser.add_argument("--initial-format", help="input file format")
    parser.add_argument("--output-format", help="format to convert the input file to")
    parser.add_argument("-c", "--config-file", help="config file in json format")
    args = parser.parse_args()

    if args.config_file is not None:
        conf_file_name = args.config_file
        config = ConfigParser()
        config.read(conf_file_name)

        input_file_name = config["info"]["input"]
        initial_format_name = config["info"]["initial_format"]
        output_format_name = config["info"]["output_format"]
    else:
        if args.input is None:
            print("you must specify the input file name")
            exit(1)
        if args.initial_format is None:
            print("you must specify the initial format")
            exit(1)
        if args.output_format is None:
            print("you must specify the output file format")
            exit(1)

        input_file_name = args.input
        initial_format_name = args.initial_format
        output_format_name = args.output_format

    convert_file(input_file_name, initial_format_name, output_format_name)
    print(
        "converted",
        input_file_name + "." + initial_format_name,
        "to",
        input_file_name + "." + output_format_name,
    )


if __name__ == "__main__":
    main()
