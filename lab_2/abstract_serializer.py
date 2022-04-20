class AbstractSerializer:
    def dumps(self, obj) -> str:
        raise NotImplementedError()

    def loads(self, string) -> object:
        raise NotImplementedError()

    def dump(self, obj, fp):
        raise NotImplementedError()

    def load(self, fp) -> object:
        raise NotImplementedError()
