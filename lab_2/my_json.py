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


def count_backslashes_before_char(string: str, index: int) -> int:
    # index is the index of the character. for example:
    # "he\\", the index of the second " is 5
    num_backslashes = 0
    i = index - 1

    while i >= 0:
        if string[i] != "\\":
            break

        num_backslashes += 1
        i -= 1

    return num_backslashes


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
                # if we have an even amount of \ before the character
                if count_backslashes_before_char(string, i) % 2 == 0:
                    inside_of_quotations = False
                    ret_str += string[i]
                    continue
        elif inside_of_quotations:
            ret_str += string[i]
        elif not inside_of_quotations:
            if string[i] != ' ' and string[i] != '\t' and string[i] != '\n':
                ret_str += string[i]

    return ret_str


def str_to_num(string: str):
    try:
        ret_num = int(string)
    except ValueError:
        ret_num = float(string)

    return ret_num


def loads_from_prepared_string(string: str) -> object:
    length = len(string)

    if string[0] == '"' and string[length - 1] == '"':
        # it is a string
        decoded_string = bytes(string[1: length - 1], "utf-8").decode("unicode_escape")
        return decoded_string
    elif string[0].isdigit():
        # is is a number (int or float)
        return str_to_num(string)
    elif string == "null":
        return None
    elif string == "true":
        return True
    elif string == "false":
        return False

    return None


def loads(string: str) -> object:
    string = delete_whitespaces_outside_of_strings(string)
    # print(string)
    return loads_from_prepared_string(string)
