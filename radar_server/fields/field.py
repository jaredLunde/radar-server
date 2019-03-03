from ..record import repr_record
from ..query import repr_query


__all__ = 'Field',


def default_cast(x):
    return x


def default_resolver(state, field_name, record=None, query=None, query_name=None, **context):
    try:
        return state[field_name]
    except (KeyError, TypeError):
        query_ref = ''

        if query_name is not None:
            query_ref = query_name
        elif query is not None:
            query_ref = f' of Query `{repr_query(query)}`'

        raise KeyError(
            f'Key `{field_name}` not found {repr_record(record)}{query_ref}.'
        )


def Field(
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
                        raise ValueError(f'Field `{name}` cannot be null.')
                    else:
                        return None
                else:
                    return default

        # setattr(resolve, 'name', key)
        setattr(resolve, 'key', key)
        return resolve

    return init


'''
from radar_server import fields
from radar_server_legacy import fields as legacy_fields
from vital.debug import Timer, Compare

Compare(fields.String, legacy_fields.String).time(1E6, key=True)

foo = fields.String()('foo')
legacy_foo = legacy_fields.String()
legacy_foo.__NAME__ = 'foo'
Compare(foo, legacy_foo.resolve).time(1E6, {'foo': 1.0})
'''