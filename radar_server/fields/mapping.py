from ..exceptions import FieldNotFound
from ..utils import to_js_key, bind
from .field import field


__all__ = 'mapping',


def mapping(**mapping_fields):
    mapping_fields = bind(mapping_fields)

    if not len(mapping_fields):
        raise ValueError('Mappings cannot be empty')

    def get_resolvers(fields):
        if not fields:
            for field_name, resolve in mapping_fields.items():
                yield to_js_key(field_name), resolve
        else:
            for field_name in fields:
                yield to_js_key(field_name), mapping_fields[field_name]

    def default_resolver(state, name, fields=None, **context):
        if state.get(name) is None:
            return None

        return {
            field_name: resolve(state[name], **context)
            for field_name, resolve in get_resolvers(fields)
        }

    def create_mapping(resolver=default_resolver, *a, key=None, **kw):
        if resolver != default_resolver:
            resolver = resolver(mapping_fields)

        if key:
            raise ValueError('Mappings cannot be Key fields.')

        return field(resolver, *a, **kw)

    return create_mapping
