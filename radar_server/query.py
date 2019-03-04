from functools import wraps
from .exceptions import RecordIsNull
from .utils import to_py_key, to_js_key, get_repr, bind


__all__ = 'query', 'query_repr'
empty_tuple = tuple()


def query_repr(interface):
    return get_repr('Record', interface)


def to_py_deep(props):
    return {
        to_py_key(key): val if not isinstance(val, dict) else to_py_deep(val)
        for key, val in props.items()
    }


def query(**fields):
    query_records = bind(fields)
    empty_requires = {record_name: None for record_name in query_records.keys()}

    def create_query(resolver):
        wrapper = wraps(resolver)

        @wrapper
        def init(query_name):
            @wrapper
            def resolve(required=None, props=None, context=None):
                context = context or {}

                if required is not None and len(required):
                    required = to_py_deep(required)

                if props is not None and len(props):
                    state = resolver(
                        required,
                        query=query_records,
                        query_name=query_name,
                        **to_py_deep(props),
                        **context
                    )
                else:
                    state = resolver(
                        required,
                        query=query_records,
                        query_name=query_name,
                        **context
                    )

                values = {}

                for record_name, required_fields in (required or empty_requires).items():
                    try:
                        result = query_records[record_name](
                            state[record_name],
                            required_fields,
                            query=query_records,
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
