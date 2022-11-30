from abc import ABC, abstractmethod
from typing import Dict, List, Protocol, Tuple


class EntryProtokoll(Protocol):
    """Protocoll for Event/Entry types.
    It has a hard requirement for published dates, altough not used directly in FeedStorage
    """

    id: int
    published: str
    published_parsed: List[int]


class FeedStorage(ABC):
    """
    Simple storage interface class, which implements some bussines logic
    to cahce the events, and handle cache updates

    _load_latest_event_by_id
    _store_event
    functions should be overwritten
    """

    # if it hit's an empty, it should check from the permanent storege, if
    # the event with the id already exists
    _cahce: Dict[int, EntryProtokoll]
    # keep track of unsaved items, not stored in the permanent storage
    _unsaved_events: List[int]

    def __init__(self) -> None:
        self._cahce = dict()
        self._unsaved_events = list()

    def get_event(self, id: int) -> EntryProtokoll | None:
        """get an event based on id

        Parameters
        ----------
        id: int
            Event/Entry id defined by the RSS feed

        Returns
        -------
        EventProtokoll
            Latest Event/Entry in observed
        """
        if id in self._cache:
            return self._cahce[id]
        loaded_event = self._load_latest_event_by_id(id)
        if loaded_event is None:
            return None
        # update cache
        self._cahce[id] = loaded_event
        return loaded_event

    def add_event(self, Event: EntryProtokoll) -> bool:
        """Adds an event to the storage

        Params
        ------
        Event: EventProtokoll
            Adds an Event/Entry to the sorage. It is lazy stored, so permanent
            storage is only used, if necesseary

        Retruns
        -------
        isUnique:bool
            If entry was not cached, or it is updated in the cache
            then returns True else returns False
        """
        index = int(Event.id)
        if index in self._cahce:
            cached = self._handle_collision(Event)
            return cached
        else:
            self._cahce[index] = Event
            self._unsaved_events.append(index)
            return True

    def _is_valid_collision(
        self, entry: EntryProtokoll
    ) -> Tuple[bool, EntryProtokoll | None]:
        index = int(entry.id)
        if index not in self._cahce:
            return (False, None)
        old_entry = self._cahce[index]
        if old_entry.published == entry.published:
            # check if entry updated, if not return.
            return (False, old_entry)
        return (True, old_entry)

    def _handle_collision(self, entry: EntryProtokoll) -> bool:
        is_real_collision, old_entry = self._is_valid_collision(entry=entry)
        if not is_real_collision:
            return False
        index = int(entry.id)
        self._store_event(old_entry)
        self._cahce[index] = entry
        self._unsaved_events.append(index)
        return True

    def flush(
        self,
    ):
        """Flush storage to permanent storage"""
        for id in self._unsaved_events:
            self._store_event(self._cahce[id])
        self._unsaved_events.clear()

    @abstractmethod
    def _store_event(self, Event: EntryProtokoll):
        ...

    @abstractmethod
    def _load_latest_event_by_id(self, id) -> EntryProtokoll | None:
        ...

    def __del__(self):
        self.flush()
