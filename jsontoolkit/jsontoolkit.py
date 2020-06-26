from jsontoolkit.utils import utils
import copy


def _action(method, data, key, index=None, value=None):
    if method is utils.Methods.GET_VALUE:
        if not index:
            return data[key]
        else:
            return data[key][index]
    elif method is utils.Methods.SET_ITEM:
        if not index:
            data[key] = value
        else:
            data[key][index] = value
    elif method is utils.Methods.DEL_ITEM:
        if not index:
            del data[key]
        else:
            del data[key][index]
    return data


def _check_for_new_item(data, key):
    keys = []
    for ind, val in enumerate(data):
        keys.extend(data[ind].keys())
    if key not in keys:
        data.append({key: {}})
    return data


def _create_ret_array(data):
    ret_val = []
    if isinstance(data, list):
        ret_val.extend(data)
    elif data:
        ret_val.append(data)
    return ret_val


def _execute(keychain, method, data, value=None):
    if isinstance(keychain, str):
        keychain = keychain.split(".")
    key_index_array = utils.get_index_from_key(keychain[0])
    key = key_index_array[0]
    index = utils.string_reps_int(key_index_array[1])
    #print(data)
    if isinstance(data, list):
        if key is '' and index is not False:
            data[index] = _execute(keychain[1:], method, data=data[index], value=value)
        else:
            ret_val = []
            if method is utils.Methods.SET_ITEM:
                data = _check_for_new_item(data, key)
            for ind, val in enumerate(data):
                data[ind] = _execute(keychain, method, data=data[ind], value=value)
                if method is utils.Methods.GET_VALUE:
                    ret_val = _create_ret_array(data[ind])
            if method is utils.Methods.GET_VALUE:
                data = ret_val
    else:
        try:
            if index is not False and isinstance(data[key], list):
                if len(keychain) == 1:
                    data = _action(method, data, key, index, value)
                else:
                    data[key][index] = _execute(keychain[1:], method,
                                                data=data[key][index],
                                                value=value)
                    if method is utils.Methods.GET_VALUE:
                        data = data[key][index]
            else:
                if len(keychain) == 1:
                    data = _action(method, data, key, value=value)
                else:
                    data[key] = _execute(keychain[1:], method, data=data[key],
                                         value=value)
                    if method is utils.Methods.GET_VALUE:
                        data = data[key]
        except KeyError:
            if method is utils.Methods.GET_VALUE:
                return {}
            else:
                pass
        except IndexError:
            if method is utils.Methods.GET_VALUE:
                return {}
            else:
                pass
    return data


class JsonToolKit:

    def __init__(self, d=None):
        self._data = d if d else {}

    def get_json(self):
        return self._data

    def set_item(self, keychain, value, data=None):
        if data:
            data = _execute(keychain, utils.Methods.SET_ITEM, data=data, value=value)
        elif not data:
            self._data = _execute(keychain, utils.Methods.SET_ITEM, data=self._data,
                                  value=value)
            data = self._data
        return data

    def del_item(self, keychain, data=None):
        if data:
            data = _execute(keychain, utils.Methods.DEL_ITEM, data=data)
        elif not data:
            self._data = _execute(keychain, utils.Methods.DEL_ITEM, data=self._data)
            data = self._data
        return data

    def get_value(self, keychain, data=None):
        ret_val = copy.deepcopy(data) if data else copy.deepcopy(self._data)
        if data:
            ret_val = _execute(keychain, utils.Methods.GET_VALUE, data=ret_val)
        elif not data:
            ret_val = _execute(keychain, utils.Methods.GET_VALUE, data=ret_val)
        return ret_val

    def get_keypaths(self, data, prefix="", start_key="", hide_arrays=True,
                     rem_dupes=True):
        ret_val = []
        if start_key:
            data = self.get_value(start_key, data)

        if isinstance(data, dict):
            for key, value in data.items():
                full_key = key if not prefix else (prefix + "." + key)
                ret_val.append(full_key)
                child_values = self.get_keypaths(value, full_key,
                                                 hide_arrays=hide_arrays)
                ret_val.extend(child_values)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                if hide_arrays:
                    child_value = self.get_keypaths(item, prefix=prefix,
                                                    hide_arrays=hide_arrays)
                else:
                    child_value = self.get_keypaths(item, prefix=prefix + f'[{index}]',
                                                    hide_arrays=hide_arrays)
                if child_value:
                    ret_val.extend(child_value)
        if rem_dupes:
            ret_val = list(set(ret_val))

        return ret_val
