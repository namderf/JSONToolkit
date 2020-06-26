from jsontoolkit.utils import utils


def _action(method, data, key, index=None, value=None):
    if method is utils.Methods.SET_ITEM:
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


def _execute(keychain, method, data, value=None):
    if isinstance(keychain, str):
        keychain = keychain.split(".")

    key_index_array = utils.get_index_from_key(keychain[0])
    key = key_index_array[0]
    index = utils.string_reps_int(key_index_array[1])

    if isinstance(data, list):
        if key is '' and index is not False:
            data[index] = _execute(keychain[1:], method, data=data[index], value=value)
        else:
            if method is utils.Methods.SET_ITEM:
                data = _check_for_new_item(data,key)
            for ind, val in enumerate(data):
                data[ind] = _execute(keychain, method, data=data[ind], value=value)
    else:
        try:
            if index is not False and isinstance(data[key], list):
                if len(keychain) == 1:
                    data = _action(method, data, key, index, value)
                else:
                    data[key][index] = _execute(keychain[1:], method,
                                                data=data[key][index],
                                                value=value)
            else:
                if len(keychain) == 1:
                    data = _action(method, data, key, value=value)
                else:
                    data[key] = _execute(keychain[1:], method, data=data[key],
                                         value=value)
        except KeyError:
            pass
    return data


class JsonToolKit:

    def __init__(self, d=None):
        self._data=d if d else {}


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

    def get_value(self, data, keychain):
        if isinstance(keychain, str):
            keychain = keychain.split(".")
        key_index_array = utils.get_index_from_key(keychain[0])
        key = key_index_array[0]
        index = utils.string_reps_int(key_index_array[1])
        if isinstance(data, list):
            if key is '' and index is not False:
                return self.get_value(data[index], keychain[1:])
            else:
                ret_val = []
                for value in data:
                    ret_value = self.get_value(value, keychain)
                    if isinstance(ret_value, list):
                        ret_val.extend(ret_value)
                    elif ret_value:
                        ret_val.append(ret_value)
            return ret_val
        else:
            try:
                if isinstance(data[key], list) and index is not False:
                    if len(keychain) == 1:
                        return (data[key][index])
                    else:
                        return self.get_value(data[key][index], keychain[1:])
                else:
                    if len(keychain) == 1:
                        return data[key]
                    else:
                        return self.get_value(data[key], keychain[1:])

            except IndexError:
                return {}
            except KeyError:
                return {}

    def get_keypaths(self, data, prefix="", start_key="", hide_arrays=True,
                     rem_dupes=True):
        ret_val = []
        if start_key:
            data = self.get_value(data, start_key)

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
