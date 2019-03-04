from radar_server import fields
from vital.debug import Timer


def bench_mapping_definition():
    Timer(fields.mapping, foo=fields.string(), bar=fields.integer()).time(1E5)


def bench_mapping_init():
    Timer(fields.mapping(foo=fields.string(), bar=fields.integer())(), 'foobar').time(1E5)


def bench_field_full_init():
    Timer(lambda: fields.mapping(foo=fields.string(), bar=fields.integer())()('foobar')).time(1E5)


def bench_field_get_value():
    foobar = fields.mapping(foo=fields.string(), bar=fields.integer())()('foobar')
    Timer(foobar, {'foobar': {'foo': 'bar', 'bar': '3'}}).time(1E5)