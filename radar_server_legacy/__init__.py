from radar_server_legacy.radar import Radar
from radar_server_legacy import fields
from radar_server_legacy.query import Query
from radar_server_legacy.action import Action
from radar_server_legacy.record import Record
from radar_server_legacy.interface import Interface
from radar_server_legacy.union import Union
from radar_server_legacy import utils
from radar_server_legacy.exceptions import QueryErrors, ActionErrors, RecordIsNull

'''

Radar ->
Query+Action (records[requested], **params)
Record (query, fields[requested], index, **params)
Field (query, record, fields[requested_within], index[record index], **params)

'''
