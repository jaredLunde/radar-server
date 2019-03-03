from .exceptions import RecordIsNull, EmptyRecordKey, MissingRecordKey
from .interface import Interface
from .utils import to_js_key, get_repr


__all__ = 'Record', 'default_resolver', 'resolve_many'


def repr_record(interface):
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


def Record(**fields):
    RecordInterface = Interface(fields)
    KEY = None

    for field_name, field in RecordInterface.items():
        if hasattr(field, 'key') and field.key is True:
            if KEY is not None:
                raise TooManyRecordKeys(
                    f'A record can only have one Key field in: {repr_record(RecordInterface)}'
                )
            KEY = field_name

    if KEY is None:
        raise MissingRecordKey(f'{repr_record(RecordInterface)} does not have a Key field.')

    def resolve_field(state, field_name, fields=None, record=None, **context):
        field = RecordInterface[field_name]

        try:
            return field(state, fields=fields, record=RecordInterface, **context)
        except RecordIsNull:
            return None

    def resolve_fields(state, fields, **context):
        if not fields:
            for field_name, field in RecordInterface.items():
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
                        f'`dict`. "{state}" is not a dict in: {repr_record(RecordInterface)}'
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
                        f'{repr_record(RecordInterface)} did not have a '
                        'Key field with a value. Your Key field must not return None.'
                    )

                return values

            return resolve_many(resolve_one) if many is True else resolve_one

        return init

    return create_record

'''
from radar_server import Record, fields

# Tests

# Record(foo=fields.String()) throws RecordKeyError
MyRecord = Record(
    foo=fields.Int(key=True),
    bar=fields.String()
)

many = MyRecord(many=True)('many')
one = MyRecord()('one')

many([{'foo': '1234', 'bar': 1234}, {'foo': '1235', 'bar': 1235}], None)
many([{'foo': '1234', 'bar': 1234}, {'foo': '1235', 'bar': 1235}], {'bar': None})
# many([{'bar': 1234}, {'bar': 1235}], {'bar': None}) throws RecordKeyError
one({'foo': '1234', 'bar': 1234}, None)
one({'foo': '1234', 'bar': 1234}, {'bar': None})

SubRecord = Record(
    id=fields.Int(key=True),
    my=MyRecord()
)

one = SubRecord()('one')
one({'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}, None)
one({'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}, {'my': None})
one({'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}, {'my': {'foo': None}})
one({'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}, {'id': None})



# Benchmarks
from vital.debug import Timer, Compare
from radar_server_legacy import Record as LegacyRecord, fields as legacy_fields

class MyLegacyRecord(LegacyRecord):
    foo = legacy_fields.Int(key=True)
    bar = legacy_fields.String()


class SubLegacyRecord(LegacyRecord):
    id = legacy_fields.Int(key=True)
    my = MyLegacyRecord()

Timer(Record, id=fields.Int(key=True), my=fields.String()).time(1E4)
Compare(MyRecord, MyLegacyRecord).time(1E6)
Timer(MyRecord()('one'), {'foo': '1234', 'bar': 1234}, None).time(1E6)
Timer(MyLegacyRecord().resolve, fields={'foo': None}, state={'foo': '1234', 'bar': 1234}).time(1E6)

Timer(SubRecord()('one'), {'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}, None).time(1E6)
slr = SubLegacyRecord()
slr.__NAME__ = 'foo'
Timer(slr.resolve, fields={'my': {}}, state={'id': '1235', 'my': {'foo': '1234', 'bar': 1234}}).time(1E6)
'''