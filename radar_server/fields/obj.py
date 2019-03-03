from ..interface import Interface
from ..exceptions import FieldNotFound
from ..utils import to_js_key
from .field import Field


__all__ = 'Obj',


def Obj(**interface_fields):
    ObjInterface = Interface(interface_fields)

    def get_resolvers(fields):
        if not fields:
            for field_name, resolve in ObjInterface.items():
                yield to_js_key(field_name), resolve
        else:
            for field_name in fields:
                yield to_js_key(field_name), ObjInterface[field_name]

    def default_resolver(state, name, fields=None, **context):
        return {
            field_name: resolve(state[name], **context)
            for field_name, resolve in get_resolvers(fields)
        }

    def create_obj(resolver=default_resolver, *a, **kw):
        return Field(resolver, *a, **kw)

    return create_obj


'''
from radar_server import fields
from radar_server_legacy import fields as legacy_fields
from vital.debug import Compare

MyObj = fields.Obj(
    foo=fields.Int(),
    bar=fields.String()
)

class MyObjLegacy(legacy_fields.Obj):
    foo = legacy_fields.Int()
    bar = legacy_fields.String()

Compare(MyObj, MyObjLegacy).time(1E6)

foobar = MyObj()('foobar')
foobar_legacy = MyObjLegacy()
foobar_legacy.__NAME__ = 'foobar'

foobar_legacy.resolve({'foobar': {'foo': '1234', 'bar': 1234}})

Compare(foobar, foobar_legacy.resolve).time(
    1E6,
    {'foobar': {'foo': '1234', 'bar': 1234}}
)

Compare(foobar, foobar_legacy.resolve).time(
    1E6,
    {'foobar': {'foo': '1234', 'bar': 1234}},
    fields={'foo': None}
)
'''
