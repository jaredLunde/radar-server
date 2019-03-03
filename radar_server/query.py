from functools import wraps
from .exceptions import RecordIsNull
from .interface import Interface
from .utils import to_py_key, to_js_key, get_repr


__all__ = 'Query', 'repr_query'
empty_tuple = tuple()


def repr_query(interface):
    return get_repr('Record', interface)


def to_py_deep(props):
    return {
        to_py_key(key): val if not isinstance(val, dict) else to_py_deep(val)
        for key, val in props.items()
    }


def Query(**fields):
    QueryInterface = Interface(fields)
    empty_requires = {record_name: None for record_name in QueryInterface.keys()}

    def create_query(resolver):
        wrapper = wraps(resolver)

        @wrapper
        def init(query_name):
            @wrapper
            def resolve(required, props=None, context=None):
                context = context or {}

                if required is not None and len(required):
                    required = to_py_deep(required)

                if props is not None and len(props):
                    state = resolver(required, **to_py_deep(props), **context)
                else:
                    state = resolver(required, **context)

                values = {}

                for record_name, required_fields in (required or empty_requires).items():
                    try:
                        result = QueryInterface[record_name](
                            state[record_name],
                            required_fields,
                            query=QueryInterface,
                            query_name=query_name,
                            **context
                        )
                    except RecordIsNull:
                        result = None

                    values[to_js_key(record_name)] = result

                return values

            return resolve

        return init

    return create_query


'''
# Tests

from radar_server import Query, Record, fields

MyRecord = Record(id=fields.Int(key=True), foo_bar=fields.String(), baz=fields.String())

@Query(my=MyRecord())
def FooQuery(records, **props):
    return {
        'my': {'id': '1234', 'foo_bar': 1234, 'baz': None}
    }

Foo = FooQuery('FooQuery')
Foo({'my': {'id': None, 'fooBar': None}})
Foo({'my': {}})
Foo(None)
Foo({})


# Bench

from vital.debug import Timer

Timer(Query, my=MyRecord()).time(1E6)
Timer(FooQuery, 'FooQuery').time(1E6)
Timer(Foo, {'my': {'fooBar': None}}).time(1E6)
'''
