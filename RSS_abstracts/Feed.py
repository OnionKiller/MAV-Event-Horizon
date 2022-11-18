from abc import ABC
from typing import List
from ..feed_handler.feed_storage import FeedStorage
from ..feed_handler.feed_consumer import FeedConsumer
from RSSEntry import RSSEntry

class Feed(object):
    storage:FeedStorage
    consumer:FeedConsumer
    def __init__(self,storage:FeedStorage,link:str) -> None:
        self.storage = storage
        self.consumer = FeedConsumer(link)
    
    def update(self)->List[RSSEntry]:
        feed_dict = self.consumer.fetch()
        new = list()

        for entry in feed_dict.entries:
            e = RSSEntry.from_dict(entry)
            unique = self.storage.add_event(e)
            if unique:
                new.append(e)

        #flush storage this could be configuration driven

        self.storage.flush()

        return new

    def list_stored(self)->List[RSSEntry]:
        #data hinding is for newbies
        return [value for _,value in self.storage._cahce.items()]

