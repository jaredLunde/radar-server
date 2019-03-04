import pytest
from radar_server import query, record, fields, RecordIsNull


Foo = record(id=fields.integer(key=True), foo=fields.string())
Bar = record(id=fields.integer(key=True), bar=fields.string())


@query(foo=Foo())
def foo_query(records, **props):
    return {
        'foo': {'id': '1234', 'foo': 'foo'}
    }


@query(foo=Foo(), bar=Bar())
def foo_bar_query(records, **props):
    return {
        'foo': {'id': '1234', 'foo': 'foo'},
        'bar': {'id': '1235', 'bar': 'bar'}
    }


def test_query_name():
    @query(foo=Foo())
    def foo_query(records, query_name=None, **props):
        assert query_name == 'foo_query'
        return {
            'foo': {'id': '1234', 'foo': 'foo'}
        }

    foo_query('foo_query')()


def test_query_resolve_one():
    values = foo_query('foo_query')()
    assert values['foo']['id'] == 1234
    assert values['foo']['foo'] == 'foo'


def test_query_resolve_all():
    values = foo_bar_query('foo_bar_query')()
    assert values['foo']['id'] == 1234
    assert values['foo']['foo'] == 'foo'
    assert values['bar']['id'] == 1235
    assert values['bar']['bar'] == 'bar'


def test_query_record_is_null():
    def raise_it(*a, **kw):
        raise RecordIsNull()

    @query(foo=Foo(raise_it), bar=Bar())
    def foo_query(records, **props):
        return {
            'foo': {'id': '1234', 'foo': 'foo'},
            'bar': {'id': '1235', 'bar': 'bar'}
        }

    values = foo_query('foo_query')(None)
    assert values['foo'] is None
    assert isinstance(values['bar'], dict)


def test_query_props():
    @query(foo=Foo())
    def foo_query(records, hello=None, **context):
        assert hello == 'world'
        return {
            'foo': {'id': '1234', 'foo': 'foo'}
        }

    foo_query('foo_bar_query')(None, {'hello': 'world'})


def test_query_context():
    @query(foo=Foo())
    def foo_query(records, request=None, **context):
        assert isinstance(request, dict)
        return {
            'foo': {'id': '1234', 'foo': 'foo'}
        }

    foo_query('foo_bar_query')(None, None, {'request': {}})


def test_query_js_keys():
    @query(foo_bar=Foo())
    def foo_bar_query(records, **props):
        return {
            'foo_bar': {'id': '1234', 'foo': 'foo'}
        }

    values = foo_bar_query('foo_bar_query')()
    assert isinstance(values['fooBar'], dict)


def test_query_py_keys():
    # require values
    @query(foo_bar=Foo())
    def foo_bar_query(records, **props):
        return {
            'foo_bar': {'id': '1234', 'foo': 'foo'}
        }

    values = foo_bar_query('foo_bar_query')({'fooBar': {'id': None}})
    assert values['fooBar']['id'] == 1234
    with pytest.raises(KeyError):
        values['fooBar']['foo']

    # prop values
    @query(foo_bar=Foo())
    def foo_bar_query(records, **props):
        assert props['hello_world'] == 'hello world'
        return {
            'foo_bar': {'id': '1234', 'foo': 'foo'}
        }

    foo_bar_query('foo_bar_query')(None, {'helloWorld': 'hello world'})


def test_query_deep_py_keys():
    @query(foo=record(id_field=fields.integer(key=True))())
    def foo_bar_query(records, **props):
        return {
            'foo': {'id_field': '1234', 'foo': 'foo'}
        }

    values = foo_bar_query('foo_bar_query')({'foo': {'idField': None}})
    assert values['foo']['idField'] == 1234
    with pytest.raises(KeyError):
        values['foo']['foo']