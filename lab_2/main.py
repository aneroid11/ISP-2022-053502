from json_serializer import JSONSerializer


def main():
    a = JSONSerializer()
    encoded = a.dumps("hello world")

    fp = open("serialized_object.json", "w")
    a.dump("hello world", fp)
    fp.close()

    fp = open("serialized_object.json", "r")
    print(a.load(fp))
    fp.close()


if __name__ == '__main__':
    main()
