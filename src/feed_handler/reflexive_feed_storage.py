from abc import ABC, abstractmethod
from typing import List
from .feed_storage import FeedStorage, EntryProtokoll


class ReflexiveFeedStorage(FeedStorage, ABC):
    def __init__(self) -> None:
        super().__init__()
        # load all events to cache
        id_list = self._load_all_event_ids()
        for id in id_list:
            event = self._load_latest_event_by_id(id)
            self.add_event(event)

    @abstractmethod
    def _load_all_event_ids(self) -> List[int]:
        ...

    @abstractmethod
    def _load_all_event_w_updates(self, id: int) -> List[EntryProtokoll]:
        ...

    def add_event(self, Event: EntryProtokoll) -> bool:
        """Adds an event to the storage

        Params
        ------
        Event: EventProtokoll
            Adds an Event/Entry to the sorage. It is immediately flushed to
            permanent storage

        Retruns
        -------
        isUnique:bool
            If entry was not cached returns True else returns False
        """
        _r = super().add_event(Event)
        self.flush()
        return _r

    def get_all_latest_events(self) -> List[EntryProtokoll]:
        return [event for _, event in self._cahce.items()]
