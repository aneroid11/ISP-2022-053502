import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from create_serializer import create_serializer


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="input file")
    parser.add_argument("-f", "--format", type=str, help="format to convert the input file to")
    parser.add_argument("-o", "--output", type=str, help="output file")
    parser.add_argument("-c", "--config-file", type=str, help="config file in json format")
    args = parser.parse_args()

    if args.config_file is not None:
        conf_file_name = args.config_file
        config = ConfigParser()
        config.read(conf_file_name)

        input_file_name = config["info"]["input"]
        output_file_name = config["info"]["output"]
        format_name = config["info"]["format"]
    else:
        if args.input is None:
            print("you must specify the input file name")
            sys.exit(1)
        if args.output is None:
            print("you must specify the output file name")
            sys.exit(1)
        if args.format is None:
            print("you must specify the format name")
            sys.exit(1)

        input_file_name = args.input
        output_file_name = args.output
        format_name = args.format

    print(input_file_name)
    print(output_file_name)
    print(format_name)


if __name__ == '__main__':
    main()
