try:
    import ujson as json
except ImportError:
    import json
import functools
from .exceptions import QueryErrors
from .interface import Interface
from .query import Query


__all__ = 'Radar',


def Radar(**queries):
    RadarInterface = Interface(queries)

    def add_query(**kw):
        query = Query(**kw)

        def wrapper(resolver):
            name = resolver.__name__
            RadarInterface[name] = functools.wraps(resolver)(query(resolver)(name))

        return wrapper

    def resolve_query(op, context):
        query = RadarInterface[op['name']]
        requires = op.get('requires')
        props = op.get('props')

        try:
            return query(requires, props, context)
        except QueryErrors as e:
            return {'isRadarError': True, error: e.for_json()}

    def resolve(ops, **context):
        ops = json.loads(ops) if isinstance(ops, str) else ops
        return [resolve_query(op, context) for op in ops]

    resolve.queries = RadarInterface
    resolve.Query = add_query
    return resolve


'''
# Test

from radar_server import Radar, Query, Record, fields

MyRecord = Record(id=fields.Int(key=True), foo_bar=fields.String(), baz=fields.String())

@Query(my=MyRecord())
def FooQuery(records, **props):
    return {
        'my': {'id': '1234', 'foo_bar': 1234, 'baz': None}
    }

radar = Radar(FooQuery=FooQuery)

@radar.Query(my_b=MyRecord())
def FooQuery(records, **props):
    return {
        'my_b': {'id': '1234', 'foo_bar': 1234, 'baz': None}
    }

radar([{'name': 'FooQuery'}])


# Bench 

from vital.debug import Timer
Timer(radar, [{'name': 'FooQuery'}]).time(1E6)
'''