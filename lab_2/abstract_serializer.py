from typing import TextIO


class AbstractSerializer:
    def dumps(self, obj: object) -> str:
        raise NotImplementedError()

    def dump(self, obj: object, fp: TextIO):
        # fp is a file descriptor, not file name
        text_to_write = self.dumps(obj)
        fp.write(text_to_write)

    def loads(self, string: str, globs: dict = None) -> object:
        raise NotImplementedError()

    def load(self, fp: TextIO, globs: dict = None) -> object:
        data_string = str(fp.read())
        return self.loads(data_string, globs)
