from .exceptions import RecordIsNull
from .record import default_resolver, resolve_many
from .utils import get_repr, to_js_key, bind


__all__ = 'union', 'union_repr'


def union_repr(interface):
    return get_repr('union', interface)


def union(resolve_member_name, **fields):
    union_members = bind(fields)

    def create_union(resolver=default_resolver, many=False):
        def init(union_name):
            def resolve_member(state, fields=None, index=None, record=None, **context):
                state = resolver(
                    state,
                    union_name,
                    fields=fields,
                    index=index,
                    record=record,
                    **context
                ) or {}

                if not isinstance(state, dict):
                    raise TypeError(
                        'Data returned by `resolver` functions must be of type `dict`. '
                        f'"{state}" is not a dict in: {union_repr(union_members)}'
                    )

                record_type = resolve_member_name(state, fields=fields, **context)

                if record_type is None:
                    raise TypeError(
                        'The `resolve_member_name` function did not return a string in: '
                        + union_repr(union_members)
                    )

                field = union_members[record_type]

                try:
                    fields = None if fields is None else fields.get(record_type)
                    return {to_js_key(record_type): field(state, fields=fields, **context)}
                except RecordIsNull:
                    return {to_js_key(record_type): None}

            resolve_ = resolve_many(resolve_member) if many is True else resolve_member
            resolve_.fields = union_members
            return resolve_

        init.fields = union_members
        return init

    create_union.fields = union_members
    return create_union

