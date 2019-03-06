import json
from radar_server import QueryErrors, resolver, query, record, fields


def create_resolver():
    return resolver(
        foo_query=query(
            foo=record(
                id=fields.integer(key=True),
                bar=fields.string()
            )(
                many=True
            )
        )(
            lambda records, bar=None, **context: ({
                'foo': [{
                    'id': '123',
                    'bar': bar
                }]
            })
        )
    )


resolve = create_resolver()


def test_resolver_query_decorator():
    resolve = create_resolver()

    @resolve.query(foo=record(id=fields.integer(key=True)))
    def Foo():
        pass

    assert resolve.queries['Foo'] is not None
    assert Foo is not None


def test_resolver_init():
    assert len(resolve.queries) == 1
    assert resolve.queries['foo_query']
    assert isinstance(resolve.query, object)


def test_resolver_resolve_one_dict():
    values = resolve({'name': 'foo_query'})
    assert isinstance(values, dict)
    assert isinstance(values['foo'], list)


def test_resolver_resolve_one():
    values = resolve([{'name': 'foo_query'}])
    assert isinstance(values, list)
    assert len(values) == 1
    assert isinstance(values[0]['foo'], list)


def test_resolver_resolve_many():
    values = resolve([{'name': 'foo_query'}, {'name': 'foo_query'}])
    assert len(values) == 2


def test_resolver_resolve_json():
    values = resolve(json.dumps([{'name': 'foo_query'}]))
    assert isinstance(values, list)
    assert len(values) == 1
    assert isinstance(values[0]['foo'], list)


def test_resolver_resolve_empty():
    values = resolve(None)
    assert values is None

    values = resolve([])
    assert len(values) == 0


def test_resolver_query_error():
    resolve = create_resolver()
    msg1 = 'Something went wrong.'
    msg2 = 'Something else went wrong.'

    @resolve.query(foo=record(id=fields.integer(key=True)))
    def Foo(*a, **kw):
        raise QueryErrors(msg1, msg2)

    values = resolve({'name': 'Foo'})
    assert len(values['error']) == 2
    assert values['isRadarError'] is True
    assert values['error'][0] == msg1
    assert values['error'][1] == msg2


def test_resolver_context():
    resolve = create_resolver()

    @resolve.query(foo=record(id=fields.integer(key=True)))
    def Foo(records, hello_world=None, **kw):
        assert hello_world == 'hello world'
        raise QueryErrors('Exit')

    resolve({'name': 'Foo'}, hello_world='hello world')