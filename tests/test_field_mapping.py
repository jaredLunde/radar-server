import pytest
from radar_server.fields import mapping, string, integer


foobar_mapping = mapping(foo=string(), bar=integer())


def test_mapping_field_cast():
    foobar = foobar_mapping()('foobar')
    values = foobar({'foobar': {'foo': 1, 'bar': '1'}})
    assert values['foo'] == '1'
    assert values['bar'] == 1


def test_mapping_null():
    foobar = foobar_mapping()('foobar')
    assert foobar({'foobar': None}) is None


def test_mapping_null_raises():
    foobar = foobar_mapping(not_null=True)('foobar')
    with pytest.raises(ValueError):
        foobar({'foobar': None})


def test_mapping_key_raises():
    with pytest.raises(ValueError):
        foobar_mapping(key=True)


def test_mapping_name():
    def resolver(foobar_mapping):
        def get_state(state, name):
            assert name == 'foobar'
        return get_state

    foobar = foobar_mapping(resolver)('foobar')
    foobar({'foobar': None})


def test_mapping_custom_resolver():
    def resolver(foobar_mapping):
        def get_state(state, name, fields=None):
            assert state[name] is True

            fake_state = {'foo': 3, 'bar': '4'}
            return {
                'foo': foobar_mapping['foo'](fake_state),
                'bar': foobar_mapping['bar'](fake_state)
            }

        return get_state

    foobar = foobar_mapping(resolver)('foobar')
    values = foobar({'foobar': True})

    assert values['foo'] == '3'
    assert values['bar'] == 4


def test_empty_raises():
    with pytest.raises(ValueError):
        mapping()