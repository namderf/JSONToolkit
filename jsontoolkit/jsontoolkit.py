from jsontoolkit.utils import utils


def execute(data, keychain, method, value=None):
    if isinstance(keychain, str):
        keychain=keychain.split(".")
    key_index_array=utils.get_index_from_key(keychain[0])
    key=key_index_array[0]
    index=utils.string_reps_int(key_index_array[1])

    if isinstance(data, list):
        if key is '' and index is not False:
            data[index]=execute(data[index],keychain[1:], method, value)
        else:
            keys = []
            if method is "add_item":
                for ind, val in enumerate(data):
                    keys.extend(data[ind].keys())
                if key not in keys:
                    data.append({key: {}})
            for ind, val in enumerate(data):
                data[ind] = execute(data[ind], keychain, method, value)
    else:
        try:
            if index is not False and isinstance(data[key], list):
                if len(keychain)==1:
                    if method is "add_item":
                        data[key][index] = value
                    elif method is "del_item":
                        del data[key][index]
                else:
                    data[key][index]=execute(data[key][index], keychain[1:], method,
                                             value)
            else:
                if len(keychain)==1:
                    if method is "add_item":
                        data[key]= value
                    elif method is "del_item":
                        del data[key]
                else:
                    data[key]=execute(data[key], keychain[1:], method, value)
        except KeyError:
            pass
    return data

def add_item(data, keychain, value):
    data= execute(data, keychain, "add_item", value)
    return data


def del_item(data, keychain):
    if isinstance(keychain, str):
        keychain = keychain.split(".")
    key_index_array = utils.get_index_from_key(keychain[0])
    key = key_index_array[0]
    index = utils.string_reps_int(key_index_array[1])
    if isinstance(data, list):
        if key is '' and index is not False:
            data[index] = del_item(data[index], keychain[1:])
        else:
            for ind, value in enumerate(data):
                data[ind]= del_item(data[ind], keychain)
    else:
        try:
            if index is not False and isinstance(data[key], list):
                if len(keychain)==1:
                    del data[key][index]
                else:
                    data[key][index]=del_item(data[key][index], keychain[1:])
            else:
                if len(keychain)==1:
                    del data[key]
                else:
                    data[key]=del_item(data[key],keychain[1:])
        except KeyError:
            pass
    return data

def get_value(data, keychain):
    if isinstance(keychain, str):
        keychain = keychain.split(".")
    key_index_array= utils.get_index_from_key(keychain[0])
    key = key_index_array[0]
    index=utils.string_reps_int(key_index_array[1])
    if isinstance(data, list):
        if key is '' and index is not False:
            return get_value(data[index], keychain[1:])
        else:
            ret_val=[]
            for value in data:
                ret_value= get_value(value, keychain)
                if isinstance(ret_value, list):
                    ret_val.extend(ret_value)
                elif ret_value:
                    ret_val.append(ret_value)

            return ret_val
    else:
        try:
            if isinstance(data[key], list) and index is not False:
                if len(keychain)==1:
                    return (data[key][index])
                else:
                    return get_value(data[key][index], keychain[1:])
            else:
                if len(keychain)==1:
                    return data[key]
                else:
                    return get_value(data[key], keychain[1:])

        except IndexError:
            return {}
        except KeyError:
            return {}


def get_keypaths(data, prefix="", start_key="", hide_arrays=True, rem_dupes=True):
    ret_val=[]
    if start_key:
        data=get_value(data, start_key)

    if isinstance(data, dict):
        for key, value in data.items():
            full_key = key if not prefix else (prefix + "." + key)
            ret_val.append(full_key)
            child_values = get_keypaths(value, full_key, hide_arrays=hide_arrays)
            ret_val.extend(child_values)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if hide_arrays:
                child_value=get_keypaths(item, prefix=prefix, hide_arrays=hide_arrays)
            else:
                child_value = get_keypaths(item, prefix=prefix+f'[{index}]',
                                            hide_arrays=hide_arrays)
            if child_value:
                ret_val.extend(child_value)
    if rem_dupes:
        ret_val= list(set(ret_val))

    return ret_val
