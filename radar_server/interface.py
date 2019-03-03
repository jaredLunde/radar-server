__all__ = 'Interface'


def Interface(fields):
    return {name: field_obj(name) for name, field_obj in fields.items()}


'''
from radar_server.interface import Interface
from radar_server import fields
from radar_server_legacy import Interface as LegacyInterface, fields as legacy_fields


MyInterface = Interface({'foo': fields.String(key=True), 'bar': fields.Int()})


class MyLegacyInterface(LegacyInterface):
    foo = legacy_fields.String(key=True)
    bar = legacy_fields.Int()


from vital.debug import Compare
Compare(
    lambda: Interface({'foo': fields.String(key=True), 'bar': fields.Int()}), 
    MyLegacyInterface
).time(1E6)
'''
