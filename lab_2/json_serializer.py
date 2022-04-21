import json
from io import FileIO
from abstract_serializer import AbstractSerializer


class JSONSerializer(AbstractSerializer):
    def __dump_class(self, obj: object) -> str:
        return '"hello world"'

    def dumps(self, obj: object) -> str:
        try:
            dumped = json.dumps(obj)
        except TypeError:
            # this is not a simple type. we need a title for the dict
            dumped = self.__dump_class(obj)

        return dumped

    def loads(self, string: str) -> object:
        return json.loads(string)

    def dump(self, obj: object, fp: FileIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def load(self, fp: FileIO) -> object:
        data_string = str(fp.read())
        return self.loads(data_string)
