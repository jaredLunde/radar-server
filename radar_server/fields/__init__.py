from .array import Array
from .field import Field
from .obj import Obj


def Bool(*a, cast=bool, **kw):
    return Field(*a, cast=cast, **kw)


def Float(*a, cast=float, **kw):
    return Field(*a, cast=cast, **kw)


def Int(*a, cast=int, **kw):
    return Field(*a, cast=cast, **kw)


def String(*a, cast=str, **kw):
    return Field(*a, cast=cast, **kw)