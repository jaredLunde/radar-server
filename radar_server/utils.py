from trie_memoize import memoize
from vital.tools import strings as string_tools


__all__ = 'get_repr', 'to_js_key', 'to_py_key'


def get_repr(name, interface):
    return f'{name}({", ".join(interface.keys())})'


@memoize(dict)
def to_js_key(key):
    camel = list(string_tools.underscore_to_camel(key))
    next_char = 0
    while True:
        try:
            char = camel[next_char]
            if char == '_':
                next_char += 1
                continue
            if char.islower():
                break
            camel[next_char] = char.lower()
            break
        except IndexError:
            break
    return ''.join(camel)


@memoize(dict)
def to_py_key(key):
    return string_tools.camel_to_underscore(key)
