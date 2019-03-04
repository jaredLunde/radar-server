import pytest
from radar_server import utils


js_terms = [
    'fooBar',
    '_fooBar',
    '_FooBar',
    '__extraPrivate',
    '__JSONPreview',
    '__foo__',
    'DONE',
    '__DONT_EDIT__',
    'FooBar',
    'fooBAR',
    'toJSONResponseObject',
    'HTTPAssetServer',
    'Bar_Foo',
    'foo____Bar',
    'BARfoo',
    'BARFoo'
]

py_terms = [
    'foo_bar',
    '_foo_bar',
    '_Foo_bar',
    '__extra_private',
    '__JSON_preview',
    '__foo__',
    'DONE',
    '__DONT_EDIT__',
    'Foo_bar',
    'foo_BAR',
    'to_JSON_response_object',
    'HTTP_asset_server',
    'Bar__foo',
    'foo_____bar',
    'BA_rfoo',
    'BAR_foo'
]

# these makes ure any incoming pythonic attrs stay that way
py_one_way_terms = [
    'foo',
    'foo_bar',
    '_foo_bar',
    'FOO_BAR',
    '_FOO_BAR',
    '__RELEASE__',
    '__release__',
]


def test_to_js_key():
    for js, py in zip(js_terms, py_terms):
        assert utils.to_js_key(py) == js


def test_to_py_key():
    for js, py in zip(js_terms, py_terms):
        assert utils.to_py_key(js) == py
    for py in py_one_way_terms:
        assert utils.to_py_key(py) == py