from .interface import Interface
from .exceptions import RecordIsNull
from .utils import get_repr, to_js_key
from .record import default_resolver, resolve_many


__all__ = 'Union', 'repr_union'


def repr_union(interface):
    return get_repr('Union', interface)


def Union(resolve_member_name, **fields):
    UnionInterface = Interface(fields)

    def create_union(resolver=default_resolver, many=False):
        def init(union_name):
            def resolve_member(state, fields=None, index=None, record=None, **context):
                state = resolver(
                    state,
                    union_name,
                    fields=fields,
                    index=index,
                    record=record,
                    **context
                ) or {}

                if not isinstance(state, dict):
                    raise TypeError(
                        'Data returned by `resolver` functions must be of type `dict`. '
                        f'"{state}" is not a dict in: {repr_union(UnionInterface)}'
                    )

                record_type = resolve_member_name(state, fields=fields, **context)

                if record_type is None:
                    raise TypeError(
                        'The `resolve_member_name` function did not return a string in: '
                        + repr_union(UnionInterface)
                    )

                field = UnionInterface[record_type]

                try:
                    fields = None if fields is None else fields.get(record_type)
                    return {to_js_key(record_type): field(state, fields=fields, **context)}
                except RecordIsNull:
                    return {to_js_key(record_type): None}

            return resolve_many(resolve_member) if many is True else resolve_member

        return init

    return create_union



'''
# Test

from radar_server import Record, Union, fields

MyRecord = Record(id=fields.Int(key=True))
MyUnion = Union(lambda state, *a, **kw: state.get('target_type'), foo=MyRecord(), bar=MyRecord())

MyUnionRecord = Record(
    id=fields.Int(key=True),
    foobar=MyUnion()
) 

one = MyUnionRecord()('foobar')
one({'id': 123456, 'foobar': {'id': 1234, 'target_type': 'foo'}}, None)
one({'id': 123456, 'foobar': {'id': 1234, 'target_type': 'bar'}}, None)


# Benchmark

from vital.debug import Timer
from radar_server_legacy import Record as LegacyRecord, Union as LegacyUnion, fields as legacy_fields

Timer(MyUnion).time(1E6)
Timer(MyUnion(), 'foobar').time(1E6)
Timer(MyUnion()('foobar'), {'id': 1234, 'target_type': 'foo'}).time(1E6)
Timer(MyUnionRecord).time(1E6)
Timer(MyUnionRecord(), 'one').time(1E6)
Timer(one, {'id': 123456, 'foobar': {'id': 1234, 'target_type': 'foo'}}, None).time(1E6)


class MyLegacyRecord(LegacyRecord):
    id = legacy_fields.Int(key=True)


class MyLegacyUnion(LegacyUnion):
    foo = MyLegacyRecord()
    bar = MyLegacyRecord()
    @staticmethod
    def get_record_type(state, *a, **kw):
        return state.get('target_type')


class MyLegacyUnionRecord(LegacyRecord):
    id = legacy_fields.Int(key=True)
    foobar = MyLegacyUnion()


mur = MyLegacyUnionRecord()
mur.__NAME__ = 'foo'
Timer(mur.resolve, fields={'foobar': {'foo': {}, 'bar': {}}}, state={'id': 123456, 'foobar': {'id': 1234, 'target_type': 'foo'}}, ).time(1E6)
'''