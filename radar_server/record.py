from .exceptions import RecordIsNull, EmptyRecordKey, MissingRecordKey, TooManyRecordKeys
from .utils import to_js_key, get_repr, bind


__all__ = 'record', 'default_resolver', 'resolve_many'


def record_repr(interface):
    return get_repr('Record', interface)


def default_resolver(state, name, index=None, **context):
    if context.get('record') is not None:
        state = state[name]
    if state is None:
        raise RecordIsNull()
    if index is None:
        return state
    else:
        return state[index]


def resolve_many(resolve_one):
    def wrapper(*a, index=None, **kw):
        index = 0
        values = []
        add_values = values.append

        while True:
            try:
                add_values(resolve_one(*a, index=index, **kw))
            except IndexError:
                break

            index += 1

        return values

    return wrapper


def record(**fields):
    record_fields = bind(fields)
    KEY = None

    for field_name, field in record_fields.items():
        if hasattr(field, 'key') and field.key is True:
            if KEY is not None:
                raise TooManyRecordKeys(
                    f'A record can only have one Key field in: {record_repr(record_fields)}'
                )
            KEY = field_name

    if KEY is None:
        raise MissingRecordKey(f'{record_repr(record_fields)} does not have a Key field.')

    def resolve_field(state, field_name, fields=None, record=None, **context):
        field = record_fields[field_name]

        try:
            return field(state, fields=fields, record=record_fields, **context)
        except RecordIsNull:
            return None

    def resolve_fields(state, fields, **context):
        if not fields:
            for field_name, field in record_fields.items():
                yield to_js_key(field_name), resolve_field(state, field_name, **context)
        else:
            fields = fields.items() if hasattr(fields, 'items') else fields

            for field_name, nested_fields in fields:
                if nested_fields is not None:
                    yield (
                        to_js_key(field_name),
                        resolve_field(state, field_name, fields=nested_fields, **context)
                    )
                else:
                    yield to_js_key(field_name), resolve_field(state, field_name, **context)

    def create_record(resolver=default_resolver, many=False):
        def init(record_name):
            def resolve_one(state, fields=None, index=None, **context):
                state = resolver(state, record_name, fields=fields, index=index, **context) or {}

                if not isinstance(state, dict):
                    raise TypeError(
                        'State returned by `resolver` functions must be of type'
                        f'`dict`. "{state}" is not a dict in: {record_repr(record_fields)}'
                    )

                values = dict(resolve_fields(state, fields, **context))
                key_name = to_js_key(KEY)

                if key_name not in values:
                    try:
                        values[key_name] = resolve_field(state, KEY, fields=fields, **context)
                    except KeyError:
                        values[key_name] = None

                if values[key_name] is None:
                    raise EmptyRecordKey(
                        f'{record_repr(record_fields)} did not have a '
                        'Key field with a value. Your Key field must not return None.'
                    )

                return values

            resolve_ = resolve_many(resolve_one) if many is True else resolve_one
            resolve_.fields = record_fields
            return resolve_

        init.fields = record_fields
        return init

    create_record.fields = record_fields
    return create_record
