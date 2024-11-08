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
        mod_dict[key_1].pop(new_value)

def add_2(mod_dict: dict[typing.Any, dict[typing.Any, typing.Any]], key_1, key_2, new_value):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    mod_dict[key_1][key_2] = new_value

def remove_2(mod_dict: dict[typing.Any, dict[typing.Any, typing.Any]], key_1, key_2):
    if key_1 not in mod_dict:
        mod_dict[key_1] = {}
    
    key_items = mod_dict[key_1]

    if key_2 in key_items:
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
        mod_dict[key_1] = {}
    
    key_items = mod_dict[key_1]

    if key_2 in key_items and new_value in key_items[key_2]:
        key_items[key_2].pop(new_value)

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