from functools import wraps
from .field import field


__all__ = 'array',


def cast_array(cast):
    @wraps(cast)
    def apply(value):
        return list(map(cast, value))
    return apply


def array(*a, cast=str, **kw):
    return field(*a, cast=cast_array(cast), **kw)