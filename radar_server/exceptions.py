class FieldNotFound(Exception):
    pass


class MissingRecordKey(Exception):
    pass


class EmptyRecordKey(Exception):
    pass


class TooManyRecordKeys(Exception):
    pass


class QueryErrors(Exception):
    def __init__(self, *messages, code=None):
        self.messages = messages

    def for_json(self):
        return [
            message if hasattr(message, 'for_json') is False else message
            for message in self.messages
        ]


class RecordIsNull(Exception):
    pass
