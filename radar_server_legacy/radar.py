try:
    import ujson as json
except ImportError:
    import json

from radar_server_legacy.exceptions import (
    QueryError,
    ActionError,
    ActionErrors,
    QueryErrors,
    OperationNotFound
)


empty_dict = {}


class Radar(object):
    __slots__ = 'queries', 'raises'

    def __init__(self, queries=None, raises=True):
        self.queries = {}
        if queries:
            self.install_query(*queries)
        self.raises = raises

    def __call__(self, state, is_json=True):
        return self.resolve(state, is_json=is_json)

    def resolver(self, *a, **kw):
        def apply(cls):
            self.install_query(cls(*a, **kw))
            return cls
        return apply

    query = resolver
    action = query

    def add(self, *queries):
        for query in queries:
            query_name = (
                query.__NAME__
                if hasattr(query, '__NAME__') else
                query.__class__.__name__
            )
            query.__NAME__ = query_name
            self.queries[query_name] = query

    install_query = add
    install_action = add

    def remove(self, *queries):
        for query in queries:
            del self.queries[query.name]

    def resolve_query(self, query_data):
        # query_requires = query_data.get('contains', empty_dict)
        query_requires = query_data.get('requires', empty_dict)
        query_params = query_data.get('props', empty_dict)
        query = self.get_query(query_data['name'])
        result = {}

        try:
            result = query.resolve(query_requires, query_params)
        except (QueryError, ActionError, ActionErrors, QueryErrors):
            result = None
        except Exception as e:
            if self.raises:
                raise e

        return result

    def resolve(self, operations, is_json=True):
        operations = json.loads(operations) \
            if isinstance(operations, str) else operations

        out = []
        add_out = out.append

        for operation in operations:
            if operation is None:
                add_out(None)
            elif operation['name'] in self.queries:
                add_out(self.resolve_query(operation))
            else:
                raise OperationNotFound(
                    f'A query with the name "{operation["name"]}" was not found.'
                )

        return out
