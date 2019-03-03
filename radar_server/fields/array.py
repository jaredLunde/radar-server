import functools
from .field import Field


__all__ = 'Array',


def cast_array(cast):
    @functools.wraps(cast)
    def apply(value):
        return list(map(cast, value))
    return apply


def Array(*a, cast=str, **kw):
    return Field(*a, cast=cast_array(cast), **kw)