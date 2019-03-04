import pytest
from radar_server.fields import array


def test_array_cast():
    foo = array(cast=float)('foo')
    assert all(map(lambda x: isinstance(x, float), foo({'foo': [-1, '1', '2.0', 3.0]})))


def test_array_null():
    foo = array()('foo')
    assert foo({'foo': None}) is None


def test_array_null_raises():
    foo = array(not_null=True)('foo')
    with pytest.raises(ValueError):
        foo({'foo': None})

    assert len(foo({'foo': []})) == 0