from json_serializer import JSONSerializer


class MyClass:
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3


def main():
    a = JSONSerializer()
    encoded = a.dumps(MyClass)
    decoded = a.loads(encoded)
    print(decoded)


if __name__ == '__main__':
    main()
