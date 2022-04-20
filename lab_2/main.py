from json_serializer import JSONSerializer


def main():
    a = JSONSerializer()
    encoded = a.dumps("hello world")

    print(a.loads(encoded))


if __name__ == '__main__':
    main()
