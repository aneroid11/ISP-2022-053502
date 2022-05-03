import converter
import json


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
    if isinstance(obj, dict):
        str_to_return = "{"
        keys = list(obj.keys())
        size = len(keys)

        for i in range(size):
            str_to_return += dumps(str(keys[i]))
            str_to_return += ": "
            str_to_return += dumps(obj[keys[i]])

            if i != size - 1:
                str_to_return += ", "

        str_to_return += "}"
        return str_to_return

    return ""


def delete_whitespaces_outside_of_strings(string: str) -> str:
    ret_str = ""
    length = len(string)
    inside_of_quotations = False

    for i in range(length):
        if string[i] == '"':
            if not inside_of_quotations:
                inside_of_quotations = True
                ret_str += string[i]
                continue
            elif inside_of_quotations:
                if string[i - 1] != "\\":
                    inside_of_quotations = False
                    ret_str += string[i]
                    continue

        if (not inside_of_quotations and string[i] != ' ' and \
                string[i] != '\t' and string[i] != '\n') or inside_of_quotations:
            ret_str += string[i]

    return ret_str


def loads(string: str) -> object:
    string = delete_whitespaces_outside_of_strings(string)
    print(string)

    return 3
