from enum import Enum


def get_index_from_key(key):
    index_start = key.find("[")
    index_end = key.find("]")
    if index_start > index_end > 0:
        index_start = index_end
    if index_start is not -1 and index_end>index_start:
        index = key[index_start + 1:index_end]
    else:
        index=None
    if index_start is not -1:
        key = key[:index_start]

    return [key, index]


def string_reps_int(input_string):
    if isinstance(input_string, str):
        try:
            return int(input_string)
        except ValueError:
            return False
        except TypeError:
            return False
    else:
        return False


def check_for_valid_index(index):
    if type(index) is int and index>-1:
        return True
    else:
        return False


class Methods(Enum):
    GET_VALUE = 1
    SET_ITEM = 2
    DEL_ITEM = 3
