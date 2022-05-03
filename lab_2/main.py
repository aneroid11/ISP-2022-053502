from create_serializer import create_serializer
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="input file")
    parser.add_argument("-f", "--format", type=str, help="format to convert the input file to")
    parser.add_argument("-o", "--output", type=str, help="output file")
    parser.add_argument("-c", "--config-file", type=str, help="config file")
    args = parser.parse_args()

    if args.config_file is not None:
        print("config_file used")
        print(args.config_file)
    else:
        print("config_file not used")
        print(args.input)
        print(args.format)
        print(args.output)


if __name__ == '__main__':
    main()
