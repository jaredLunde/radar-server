import pytest
from radar_server import union, record, fields


Foo = record(id=fields.integer(key=True))
Bar = record(id=fields.string(key=True))
FooBarUnion = union(
    lambda state, *a, **kw: state.get('type'),
    foo=Foo(),
    bar=Bar()
)


def test_union_name():
    def resolve_name(state, name, **kw):
        assert name == 'foobar'
        return state

    foobar = union(
        lambda state, *a, **kw: state.get('type'),
        a=record(id=fields.integer(key=True))()
    )(resolve_name)('foobar')

    foobar({'id': 1234, 'type': 'a'}, {'id': None})


def test_union_resolve_member():
    foobar = FooBarUnion()('foobar')

    values = foobar({'id': 1234, 'type': 'foo'}, {'id': None})
    assert isinstance(values['foo']['id'], int)
    with pytest.raises(KeyError):
        values['bar']

    values = foobar({'id': 1234, 'type': 'bar'}, {'id': None})
    assert isinstance(values['bar']['id'], str)
    with pytest.raises(KeyError):
        values['foo']


def test_union_resolve_member_many():
    foobar = FooBarUnion(many=True)('foobar')

    values = foobar([{'id': 1234, 'type': 'foo'}], {'id': None})
    assert isinstance(values[0]['foo']['id'], int)
    with pytest.raises(KeyError):
        values[0]['bar']

    values = foobar([{'id': 1234, 'type': 'bar'}], {'id': None})
    assert isinstance(values[0]['bar']['id'], str)
    with pytest.raises(KeyError):
        values[0]['foo']

    values = foobar([{'id': 1234, 'type': 'foo'}, {'id': 1234, 'type': 'bar'}], {'id': None})
    assert isinstance(values[0]['foo']['id'], int)
    with pytest.raises(KeyError):
        values[0]['bar']
    assert isinstance(values[1]['bar']['id'], str)
    with pytest.raises(KeyError):
        values[1]['foo']


def test_union_bad_member_resolver():
    FooBarUnion = union(
        lambda state, *a, **kw: None,
        foo=Foo(),
        bar=Bar()
    )
    foobar = FooBarUnion()('foobar')

    with pytest.raises(TypeError):
        foobar({'id': 1234, 'type': 'bar'})


def test_union_js_keys():
    FooBarUnion = union(
        lambda state, *a, **kw: state.get('type'),
        foo_bar=Foo(),
        bar_baz=Bar()
    )
    foobar = FooBarUnion()('foobar')

    values = foobar({'id': 1234, 'type': 'foo_bar'})
    assert values['fooBar']['id'] == 1234

    values = foobar({'id': 1234, 'type': 'bar_baz'})
    assert values['barBaz']['id'] == '1234'