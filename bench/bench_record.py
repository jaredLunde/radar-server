from radar_server import record, fields
from vital.debug import Timer


def bench_record_definition():
    Timer(record, foo=fields.string(key=True), bar=fields.integer()).time(1E5)


def bench_record_create():
    Timer(record(foo=fields.string(key=True), bar=fields.integer())).time(1E5)


def bench_record_init():
    rec = record(foo=fields.string(key=True), bar=fields.integer())()
    Timer(rec, 'foo').time(1E5)


def bench_record_full_init():
    Timer(lambda: record(foo=fields.string(key=True), bar=fields.integer())()('foo')).time(1E5)


def bench_record_resolve_all():
    foo = record(foo=fields.string(key=True), bar=fields.integer())()('foo')
    Timer(foo, {'foo': 'bar', 'bar': 1234}).time(1E5)


def bench_record_resolve_one():
    foo = record(foo=fields.string(key=True), bar=fields.integer())()('foo')
    Timer(foo, {'foo': 'bar'}, {'foo': None}).time(1E5)


def bench_record_resolve_many():
    foo = record(foo=fields.string(key=True), bar=fields.integer())(many=True)('foo')
    Timer(foo, [{'foo': 'bar', 'bar': 1234}]).time(1E5)


def bench_record_nested():
    foobar = record(
        foo=fields.string(key=True),
        bar=record(baz=fields.integer(key=True))()
    )()('foobar')
    Timer(foobar, {'foo': 'bar', 'bar': {'baz': 1234}}).time(1E5)
