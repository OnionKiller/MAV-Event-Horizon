from parser.MAV.feed_parser import FeedParser
from feed_handler.feed_consumer import FeedConsumer

import hug

from db import SqlAlchemyContext


@hug.get("/test-db")
def test_db(db:SqlAlchemyContext):
    Feed = FeedConsumer()
    d = Feed.fetch()
    entry = FeedParser.parse_entry(d.entries[0])
    entry_dump = FeedParser.dump_entry(d.entries[0],entry.uuid)
    db.add_all([entry,entry_dump])
    db.commit()