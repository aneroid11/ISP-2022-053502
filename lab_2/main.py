from create_serializer import create_serializer
import argparse
from configparser import ConfigParser


def main():
    conf = ConfigParser()
    conf["info"] = {"input": "serialized_object.json",
                    "output": "serialized_object.toml",
                    "format": "yaml"}
    with open('config.ini', 'w') as configfile:
        conf.write(configfile)

    """parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="input file")
    parser.add_argument("-f", "--format", type=str, help="format to convert the input file to")
    parser.add_argument("-o", "--output", type=str, help="output file")
    parser.add_argument("-c", "--config-file", type=str, help="config file in json format")
    args = parser.parse_args()

    if args.config_file is not None:
        print("config_file used")
        conf_file_name = args.config_file
        file = open(conf_file_name)
        json_serializer = create_serializer("json")
    else:
        print("config_file not used")
        print(args.input)
        print(args.format)
        print(args.output)"""


if __name__ == '__main__':
    main()
