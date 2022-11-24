from typing import List
from ..RSS_abstracts.RSSEntry import RSSEntry

from .reflexive_feed_storage import ReflexiveFeedStorage


class DictStorage(ReflexiveFeedStorage):
    _storage = dict()

    def _load_all_event_ids(self) -> List[int]:
        return self._storage.keys()

    def _load_all_event_w_updates(self, id: int) -> List[RSSEntry]:
        raise NotImplementedError()

    def _store_event(self, Event: RSSEntry):
        self._storage[Event.id] = Event

    def _load_latest_event_by_id(self, id) -> RSSEntry | None:
        return self._storage[id]
