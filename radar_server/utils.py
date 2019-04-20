from trie_memoize import memoize


__all__ = 'bind', 'get_repr', 'to_js_key', 'to_py_key', 'to_py_deep'


def bind(fields):
    return {name: field_obj(name) for name, field_obj in fields.items()}


def get_repr(name, interface):
    return f'{name}({", ".join(interface.keys())})'


@memoize(dict)
def to_js_key(key):
    if key.isupper():
        return key

    r = key[0]
    has_alpha = False
    for i, char in enumerate(key[1:], 1):
        if char.isupper():
            r += char
            has_alpha = True
        elif char == '_':
            try:
                next_char = key[i + 1]
            except IndexError:
                next_char = False
            try:
                prev_char = key[i - 1]
            except IndexError:
                prev_char = False
            if next_char and next_char != '_' and prev_char != '_':
                continue
            else:
                r += char
        else:
            try:
                prev_char = key[i - 1]
            except IndexError:
                prev_char = False
            try:
                prev_r_char = r[-1]
            except:
                prev_r_char = False
            if prev_char == '_' and has_alpha:
                if prev_r_char == '_':
                    r = r[:-1]
                r += char.upper()
            else:
                r += char
            has_alpha = True
    return r


@memoize(dict)
def to_py_key(key):
    if key.isupper() or key.islower():
        return key

    r = key[0]
    has_alpha = False

    for i, char in enumerate(key[1:], 1):
        if char.isupper():
            try:
                prev_char = key[i - 1]
            except IndexError:
                prev_char = False

            if has_alpha is False and prev_char == '_':
                r += char
                has_alpha = True
                continue

            try:
                if key[i + 1].isupper() and prev_char:
                    if not prev_char.isupper() and key[i - 1]:
                        r += '_'
                    r += char
                    has_alpha = True
                    continue
            except IndexError:
                pass
            try:
                if prev_char.isupper() and (i == len(key) - 1 or key[i + 1] == '_'):
                    r += char
                    has_alpha = True
                    continue
                if prev_char.islower() or key[i + 1].islower():
                    r += '_'
            except IndexError:
                pass

            has_alpha = True

        if char != '_':
            has_alpha = True
        r += char.lower()
    return r


def to_py_deep(props):
    return {
        to_py_key(key): val if not isinstance(val, dict) else to_py_deep(val)
        for key, val in props.items()
    }
