import pytest
from radar_server import (
    record,
    fields,
    MissingRecordKey,
    EmptyRecordKey,
    FieldNotFound,
    TooManyRecordKeys,
    RecordIsNull
)


FoobarRecord = record(
    foo=fields.integer(key=True),
    bar=fields.string()
)


def test_missing_key_raises():
    with pytest.raises(MissingRecordKey):
        record(foo=fields.string())


def test_too_many_keys_raises():
    with pytest.raises(TooManyRecordKeys):
        record(foo=fields.string(key=True), bar=fields.string(key=True))


def test_empty_key_raises():
    foobar = FoobarRecord()('foobar')
    with pytest.raises(EmptyRecordKey):
        foobar({'bar': 'foo', 'foo': None})

    with pytest.raises(EmptyRecordKey):
        foobar({'bar': 'foo'}, {'bar': None})


def test_empty_requested_value_raises():
    foobar = FoobarRecord()('foobar')
    with pytest.raises(KeyError):
        foobar({'foo': 1234})


def test_record_is_null():
    foobar = FoobarRecord()('foobar')
    with pytest.raises(RecordIsNull):
        foobar(None)


def test_record_name():
    def resolve_name(state, name, **kw):
        assert name == 'foobar'
        return state

    foobar = FoobarRecord(resolve_name)('foobar')
    foobar({'foo': 1234}, {'foo': None})


def test_resolve_one():
    foobar = FoobarRecord()('foobar')
    # value picking
    values = foobar({'foo': '1234'}, {'foo': None})
    with pytest.raises(KeyError):
        values['bar']
    assert values.get('foo') == 1234
    # implicit key fetching
    values = foobar({'foo': 1234, 'bar': 1234}, {'bar': None})
    assert values.get('foo') == 1234
    assert values.get('bar') == '1234'
    # fetch all
    values = foobar({'foo': 1234, 'bar': 1234})
    assert values.get('foo') == 1234
    assert values.get('bar') == '1234'
    values = foobar({'foo': 1234, 'bar': 1234}, {})
    assert values.get('foo') == 1234
    assert values.get('bar') == '1234'


def test_resolve_many():
    foobar = FoobarRecord(many=True)('foobar')
    # value picking
    values = foobar([{'foo': '1234'}], {'foo': None})
    assert isinstance(values, list)
    assert len(values) == 1
    with pytest.raises(KeyError):
        values[0]['bar']
    assert values[0].get('foo') == 1234
    # index errors
    with pytest.raises(KeyError):
        foobar({'foo': '1234'}, {'foo': None})
    # implicit key fetching
    values = foobar([{'foo': 1234, 'bar': 1234}], {'bar': None})
    assert values[0].get('foo') == 1234
    assert values[0].get('bar') == '1234'
    # fetch all
    values = foobar([{'foo': 1234, 'bar': 1234}])
    assert values[0].get('foo') == 1234
    assert values[0].get('bar') == '1234'
    values = foobar([{'foo': 1234, 'bar': 1234}], {})
    assert values[0].get('foo') == 1234
    assert values[0].get('bar') == '1234'


def test_js_keys():
    rec = record(
        foo_bar=fields.integer(key=True),
        bar_baz_boz=fields.string()
    )
    # single record
    cases = rec()('cases')
    values = cases({'foo_bar': 1234, 'bar_baz_boz': 'foo'})
    assert values.get('fooBar') == 1234
    assert values.get('barBazBoz') == 'foo'
    # many records
    cases = rec(many=True)('cases')
    values = cases([{'foo_bar': 1234, 'bar_baz_boz': 'foo'}])
    assert values[0].get('fooBar') == 1234
    assert values[0].get('barBazBoz') == 'foo'


def test_nested_record_resolve_one():
    rec = record(
        foo=fields.integer(key=True),
        bar=record(baz=fields.string(key=True))()
    )
    foobar = rec()('foobar')
    # value picking
    values = foobar({'foo': '1234'}, {'foo': None})
    with pytest.raises(KeyError):
        values['bar']
    assert values.get('foo') == 1234
    # implicit key fetching
    values = foobar({'foo': 1234, 'bar': {'baz': 1234}}, {'bar': None})
    assert values.get('foo') == 1234
    assert values['bar']['baz'] == '1234'
    values = foobar({'foo': 1234, 'bar': {'baz': 1234}}, {'bar': {}})
    assert values.get('foo') == 1234
    assert values['bar']['baz'] == '1234'
    # fetch all
    values = foobar({'foo': 1234, 'bar': {'baz': 1234}})
    assert values.get('foo') == 1234
    assert values['bar']['baz'] == '1234'
    values = foobar({'foo': 1234, 'bar': {'baz': 1234}}, {})
    assert values.get('foo') == 1234
    assert values['bar']['baz'] == '1234'


def test_nested_record_resolve_many():
    rec = record(
        foo=fields.integer(key=True),
        bar=record(baz=fields.string(key=True))(many=True)
    )
    foobar = rec()('foobar')
    # value picking
    values = foobar({'foo': '1234'}, {'foo': None})
    with pytest.raises(KeyError):
        values['bar']
    assert values.get('foo') == 1234
    # implicit key fetching
    values = foobar({'foo': 1234, 'bar': [{'baz': 1234}]}, {'bar': None})
    assert values.get('foo') == 1234
    assert values['bar'][0]['baz'] == '1234'
    # fetch all
    values = foobar({'foo': 1234, 'bar': [{'baz': 1234}]})
    assert values.get('foo') == 1234
    assert values['bar'][0]['baz'] == '1234'
    values = foobar({'foo': 1234, 'bar': [{'baz': 1234}]}, {})
    assert values.get('foo') == 1234
    assert values['bar'][0]['baz'] == '1234'


def test_record_resolver_returns_dict():
    def resolve_bad(state, name, **kw):
        return 1

    foobar = FoobarRecord(resolve_bad)('foobar')
    with pytest.raises(TypeError):
        foobar({'foo': 0})

    def resolve_list(state, name, **kw):
        return [state]

    foobar = FoobarRecord(resolve_list)('foobar')
    with pytest.raises(TypeError):
        foobar({'foo': 0})
