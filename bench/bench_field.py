from radar_server import fields
from vital.debug import Timer


def bench_field_definition():
    Timer(fields.field).time(1E5)


def bench_field_definition_with_params():
    Timer(fields.field, key=True, cast=str).time(1E5)


def bench_field_init():
    Timer(fields.field(), 'foo').time(1E5)


def bench_field_full_init():
    Timer(lambda: fields.field()('foo')).time(1E5)


def bench_field_get_value():
    foo = fields.field()('foo')
    Timer(foo, {'foo': 'bar'}).time(1E5)