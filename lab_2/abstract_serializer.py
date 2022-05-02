from typing import TextIO


class AbstractSerializer:
    def dumps(self, obj: object) -> str:
        raise NotImplementedError()

    def dump(self, obj: object, fp: TextIO):
        raise NotImplementedError()

    def loads(self, string: str, globs: dict = None) -> object:
        raise NotImplementedError()

    def load(self, fp: TextIO, globs: dict = None) -> object:
        raise NotImplementedError()
