from abstract_serializer import AbstractSerializer


class JSONSerializer(AbstractSerializer):
    def dumps(self, obj) -> str:
        return "jsonjsonjsonjson"

    def loads(self, string) -> object:
        return int(5555555555555284329895932859968938592436982396829385928394589235893892893842959)

    def dump(self, obj, fp):
        print("dump(obj, fp)")

    def load(self, fp) -> object:
        return int(22305692049306823096093206932095029604329069309240590)
