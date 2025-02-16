
def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}

print(merge_dicts({'a': 1, 'b': 2}, {'b': 3, 'c': 4}))