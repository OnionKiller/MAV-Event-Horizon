import logging
from time import mktime
from datetime import datetime

from parser.MAV.models import MAVEvent,MAVEventDump

class FeedParser(object):
    @staticmethod
    def parse_entry(feedEntry)->MAVEvent:
        try:
            event = MAVEvent(
                id = feedEntry['id'],
                title = feedEntry['title'],
                last_modification = datetime.fromtimestamp(mktime(feedEntry['published_parsed'])),
            )
        except ValueError as e:
            logging.error(f"Feed is missing a field: {str(e)}. \n feedEntry : {str(feedEntry)}")
            #raise error anyway, but note the location, where it occured
            raise e
        return event

    @staticmethod
    def dump_entry(feedEntry,uuid)->MAVEventDump:
        return MAVEventDump(
            event_dict = feedEntry,
            event_uuid = uuid
        )
        