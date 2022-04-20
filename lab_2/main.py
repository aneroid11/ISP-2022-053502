from abstract_serializer import AbstractSerializer


def main():
    a = AbstractSerializer()
    encoded = a.dumps("hello world")

    print(a.loads(encoded))


if __name__ == '__main__':
    main()
