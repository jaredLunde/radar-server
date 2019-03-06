from .array import array
from .field import field
from .mapping import mapping


def boolean(*a, cast=bool, **kw):
    return field(*a, cast=cast, **kw)


def single(*a, cast=float, **kw):
    return field(*a, cast=cast, **kw)


def integer(*a, cast=int, **kw):
    return field(*a, cast=cast, **kw)


def string(*a, cast=str, **kw):
    return field(*a, cast=cast, **kw)
