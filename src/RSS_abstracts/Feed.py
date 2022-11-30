from abc import ABC
from typing import List
from ..feed_handler.reflexive_feed_storage import ReflexiveFeedStorage
from ..feed_handler.feed_consumer import FeedConsumer
from .RSSEntry import RSSEntry


class Feed(object):
    _storage: ReflexiveFeedStorage
    _consumer: FeedConsumer

    def __init__(self, storage: ReflexiveFeedStorage, link: str) -> None:
        self._storage = storage
        self._consumer = FeedConsumer(link)

    def update(self) -> List[RSSEntry]:
        """
        Updates feed.
        Returns
        -------
        updated_entries:List[RSSEntry]
            A list with the Entries which are new.
        """
        feed_dict = self._consumer.fetch()
        new = list()

        for entry in feed_dict.entries:
            e = RSSEntry.from_dict(entry)
            unique = self._storage.add_event(e)
            if unique:
                new.append(e)

        return new

    def list_entries(self) -> List[RSSEntry]:
        """Lists all the entries stored in the feed, using the latest entry for all ids
        Returns
        -------
        all_entries:List[RSSEntry]
            A list of stored entries, where all entries are the latest form unique ids.
        """
        return self._storage.get_all_latest_events()

    def list_entries_updates(self) -> List[List[RSSEntry]]:
        """Lists all the entries stored in the feed
        Returns
        -------
        all_entries:List[List[RSSEntry]]
            A  nested list of stored entries, where each list stores all the entries from the same ids.
        """
        _r = list()
        ids = self._storage._load_all_event_ids()
        for id in ids:
            _r.append(self._storage._load_all_event_w_updates(id))
        return _r
