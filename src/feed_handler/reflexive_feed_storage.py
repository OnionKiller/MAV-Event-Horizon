from abc import ABC, abstractmethod
from typing import List
from .feed_storage import FeedStorage, EntryProtokoll


class ReflexiveFeedStorage(FeedStorage, ABC):
    _already_stored_events = list()

    def __init__(self) -> None:
        super().__init__()
        # load all events to cache
        id_list = self._load_all_event_ids()
        for id in id_list:
            event = self._load_latest_event_by_id(id)
            self._cahce[event.id] = event
            self._already_stored_events.append(id)

    @abstractmethod
    def _load_all_event_ids(self) -> List[int]:
        ...

    @abstractmethod
    def _load_all_event_w_updates(self, id: int) -> List[EntryProtokoll]:
        ...

    def add_event(self, event: EntryProtokoll) -> bool:
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
        # workaround for already stored, and loaded events
        if (
            self._is_valid_collision(event)
            and event.id in self._already_stored_events
        ):
            # if it is a collision, it would save the already saved element. so we need to remove that.
            # now it's not in the cache, but we know it will be replaced later. It is a workaround
            # necessary becous how the cahce collision is implemented. data hiding is broken several
            # times, but python doesn't cares
            self._cahce.pop(event.id)
            self._already_stored_events.remove(event.id)

        _r = super().add_event(event)
        self.flush()
        return _r

    def get_all_latest_events(self) -> List[EntryProtokoll]:
        return [event for _, event in self._cahce.items()]
