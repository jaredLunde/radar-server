import pytest
from radar_server.fields import field


def test_key():
    foo = field()('foo')
    assert foo.key is False

    foo = field(key=True)('foo')
    assert foo.key is True


def test_cast():
    foo = field(cast=float)('foo')
    assert isinstance(foo({'foo': '1.2'}), float)


def test_name():
    def resolver(state, name):
        assert name == 'foo'

    foo = field(resolver)
    foo('foo')({})


def test_default_resolver_raises():
    foo = field()('foo')

    with pytest.raises(KeyError):
        foo({'bar': '1.2'})


def test_default_resolver_context():
    def resolver(state, name, special=None):
        assert special == 'bar'

    foo = field(resolver)('foo')
    foo({'foo': None}, special='bar')


def test_not_null_raises():
    foo = field(not_null=True)('foo')

    with pytest.raises(ValueError):
        foo({'foo': None})


def test_not_null_passes():
    foo = field(not_null=False)('foo')
    assert foo({'foo': None}) is None


def test_default():
    foo = field(default='foo')('foo')
    assert foo({'foo': None}) == 'foo'