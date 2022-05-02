import converter


def is_not_collection(obj: object) -> bool:
    return not isinstance(obj, dict) and not isinstance(obj, list) and \
           not isinstance(obj, tuple)


def dumps(obj: object) -> str:
    if is_not_collection(obj):
        if obj is None:
            return 'null'
        if isinstance(obj, bool):
            if obj:
                return 'true'
            return 'false'
        if isinstance(obj, str):
            return f'"{obj}"'
        if isinstance(obj, int) or isinstance(obj, float):
            return f'{obj}'

    if isinstance(obj, tuple):
        obj = converter.tuple_to_list_recursive(obj)
    if isinstance(obj, list):
        str_to_return = '['

        size = len(obj)
        for i in range(size):
            str_to_return += dumps(obj[i])
            if i != size - 1:
                str_to_return += ', '

        str_to_return += ']'
        return str_to_return

    return '"3"'


def loads(string: str) -> object:
    return 3
