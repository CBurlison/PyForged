import typing

def add(mod_dict: dict, key_1, new_value):
    mod_dict[key_1] = new_value

def add_list(mod_dict: dict[typing.Any, list[typing.Any]], key_1, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = [new_value]
    else:
        mod_dict[key_1].append(new_value)

def remove_list(mod_dict: dict[typing.Any, list[typing.Any]], key_1, new_value):
    if key_1 in mod_dict and new_value in mod_dict[key_1]:
        mod_dict[key_1].remove(new_value)

def add_2(mod_dict: dict[typing.Any, dict[typing.Any, typing.Any]], key_1, key_2, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    mod_dict[key_1][key_2] = new_value

def remove_2(mod_dict: dict[typing.Any, dict[typing.Any, typing.Any]], key_1, key_2):
    if key_1 not in mod_dict:
        return
    
    key_items = mod_dict[key_1]

    if key_2 in key_items:
        key_items.pop(key_2)

    if len(key_items) == 0:
        mod_dict.pop(key_1)

def add_3(mod_dict: dict[typing.Any, dict[typing.Any, dict[typing.Any, typing.Any]]], key_1, key_2, key_3, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    item = mod_dict[key_1]

    if key_1 not in item:
        item[key_2] = {}

    item[key_2][key_3] = new_value

def remove_3(mod_dict: dict[typing.Any, dict[typing.Any, dict[typing.Any, typing.Any]]], key_1, key_2, key_3):
    if key_1 not in mod_dict:
        return
    
    key_items = mod_dict[key_1]

    if key_2 in key_items:
        key_items_2 = mod_dict[key_1]

        if key_3 in key_items_2:
            key_items_2.pop(key_3)

        if len(key_items_2) == 0:
            key_items.pop(key_2)

    if len(key_items) == 0:
        mod_dict.pop(key_1)

def add_list_2(mod_dict: dict[typing.Any, dict[typing.Any, list[typing.Any]]], key_1, key_2, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    key_items = mod_dict[key_1]

    if key_2 not in key_items:
        key_items[key_2] = [new_value]
    else:
        key_items[key_2].append(new_value)

def remove_list_2(mod_dict: dict[typing.Any, dict[typing.Any, list[typing.Any]]], key_1, key_2, new_value):
    if key_1 not in mod_dict:
        return
    
    key_items = mod_dict[key_1]

    if key_2 in key_items and new_value in key_items[key_2]:
        item_list = key_items[key_2]
        item_list.remove(new_value)

        if len(item_list) == 0:
            key_items.pop(key_2)

    if len(key_items) == 0:
        mod_dict.pop(key_1)

def insert(mod_dict: dict[typing.Any, list[typing.Any]], index: int, key_1, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = [new_value]
    else:
        mod_dict[key_1].insert(index, new_value)

def insert_2(mod_dict: dict[typing.Any, dict[typing.Any, list[typing.Any]]], index: int, key_1, key_2, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    key_items = mod_dict[key_1]

    if key_2 not in key_items:
        key_items[key_2] = [new_value]
    else:
        key_items[key_2].insert(index, new_value)

def increment(mod_dict: dict[typing.Any, int], key_1, amount: int = 1) -> int:
    if key_1 not in mod_dict:
        mod_dict[key_1] = amount
    else:
        mod_dict[key_1] += amount

    return mod_dict[key_1]

def increment_2(mod_dict: dict[typing.Any, dict[typing.Any, int]], key_1, key_2, amount: int = 1) -> int:
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    key_items = mod_dict[key_1]

    if key_2 not in key_items:
        key_items[key_2] = amount
    else:
        key_items[key_2] += amount

    return key_items[key_2]