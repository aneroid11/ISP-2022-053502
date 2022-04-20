from io import FileIO


class AbstractSerializer:
    def dumps(self, obj: object) -> str:
        raise NotImplementedError()

    def loads(self, string: str) -> object:
        raise NotImplementedError()

    def dump(self, obj: object, fp: FileIO):
        raise NotImplementedError()

    def load(self, fp: FileIO) -> object:
        raise NotImplementedError()
