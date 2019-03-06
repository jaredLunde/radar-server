try:
    import ujson as json
except ImportError:
    import json
import functools
from .exceptions import QueryErrors
from .query import query as create_query
from .utils import bind


__all__ = 'resolver',


def resolver(**queries):
    radar_queries = bind(queries)

    def add_query(**kw):
        query = create_query(**kw)

        def wrapper(resolver):
            name = resolver.__name__
            radar_queries[name] = functools.wraps(resolver)(query(resolver)(name))
            return radar_queries[name]

        return wrapper

    def resolve_query(op, context):
        query = radar_queries[op['name']]
        requires = op.get('requires')
        props = op.get('props')

        try:
            return query(requires, props, context)
        except QueryErrors as e:
            return {'isRadarError': True, 'error': e.for_json()}

    def resolve(ops, **context):
        ops = json.loads(ops) if isinstance(ops, str) else ops

        if not ops:
            return ops

        if isinstance(ops, dict):
            return resolve_query(ops, context)
        else:
            return [resolve_query(op, context) for op in ops]

    resolve.queries = radar_queries
    resolve.query = add_query
    return resolve
