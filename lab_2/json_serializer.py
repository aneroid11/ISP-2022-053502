from abstract_serializer import \
    AbstractSerializer, dumps_using_dumps_elementary, loads_using_loads_elementary
# import json
import my_json as json


def json_dumps_elementary(elem_obj: object):
    return json.dumps(elem_obj)


def json_loads_elementary(elem_str: str) -> object:
    return json.loads(elem_str)


class JSONSerializer(AbstractSerializer):
    def dumps(self, obj: object) -> str:
        return dumps_using_dumps_elementary(obj, json_dumps_elementary)

    def loads(self, string: str, globs: dict = None) -> object:
        return loads_using_loads_elementary(string, json_loads_elementary, globs)
