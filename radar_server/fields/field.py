from ..record import record_repr
from ..query import query_repr


__all__ = 'field',


def default_cast(x):
    return x


def default_resolver(state, field_name, record=None, query=None, query_name=None, **context):
    try:
        return state[field_name]
    except (KeyError, TypeError):
        query_ref = ''
        record_ref = ''

        if query_name is not None:
            query_ref = query_name
        elif query is not None:
            query_ref = f' of {query_repr(query)}'
        if record is not None:
            record_ref = f' in {record_repr(record)}'
        raise KeyError(f'Field `{field_name}` not found{record_ref}{query_ref}.')


def field(
    resolver=default_resolver,
    default=None,
    cast=default_cast,
    not_null=False,
    key=False,
):
    def init(name):
        def resolve(state, **context):
            value = resolver(state, name, **context)

            if value is not None:
                return cast(value)
            else:
                if default is None:
                    if not_null:
                        raise ValueError(f'field `{name}` cannot be null.')
                    else:
                        return None
                else:
                    return default

        # setattr(resolve, 'name', key)
        resolve.key = key
        return resolve

    return init

