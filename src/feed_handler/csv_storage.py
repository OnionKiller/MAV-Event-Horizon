from datetime import datetime
from pathlib import Path
from time import mktime, strptime
from typing import List
from .reflexive_feed_storage import ReflexiveFeedStorage
from ..RSS_abstracts.RSSEntry import RSSEntry

import pandas as pd


class csvStorage(ReflexiveFeedStorage):
    _storage: pd.DataFrame
    _csv_path: Path

    def __init__(self, file_location: Path) -> None:
        if not isinstance(file_location, Path):
            file_location = Path(file_location)

        if file_location.suffix != ".csv":
            raise ValueError(f"Path {file_location} is not a csv file.")

        if file_location.exists():
            df = pd.read_csv(file_location, index_col=False)
            # map datetime string to actual datetime
            df["published_datetime"] = df["published_datetime"].transform(
                lambda x: datetime.fromtimestamp(
                    mktime(strptime(x, "%Y-%m-%d %H:%M:%S"))
                )
            )
            # map str representation of time struct to actual time struct
            df["published_parsed"] = df["published_datetime"].transform(
                lambda x: x.timetuple()
            )
            self._storage = df

        else:
            self._storage = pd.DataFrame()

        self._csv_path = file_location

        super().__init__()

    def _convert(_, df: pd.DataFrame) -> List[RSSEntry]:
        dicts = df.to_dict(orient="records")
        _return = list()
        for d in dicts:
            entry = RSSEntry.from_dict(d)
            entry.unparsed = d["unparsed"]
            _return.append(entry)
        return _return

    def _load_all_event_ids(self) -> List[int]:
        if self._storage.empty:
            return list()
        return self._storage.id.unique()

    def _load_all_event_w_updates(self, id: int) -> List[RSSEntry]:
        if self._storage.empty:
            return list()
        return self._convert(self._storage[self._storage.id == id])

    def _store_event(self, Event: RSSEntry):
        # create df
        df_tmp = pd.DataFrame([Event])
        df_tmp["published_datetime"] = datetime.fromtimestamp(
            mktime(Event.published_parsed)
        )

        # append data
        self._storage = pd.concat([self._storage, df_tmp])

        # sort by update time
        self._storage = self._storage.sort_values(
            "published_datetime", ascending=False
        )

        self._storage.to_csv(self._csv_path, index=False)

    def _load_latest_event_by_id(self, id) -> RSSEntry | None:
        list = self._load_all_event_w_updates(id)
        if len(list) == 0:
            return None
        return list[0]
