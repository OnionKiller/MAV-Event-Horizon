from dataclasses import dataclass, field
from datetime import datetime
import time
from typing import Dict
from feedparser import FeedParserDict


@dataclass(match_args=True)
class RSSEntry(object):
    id: int
    title: str
    link: str
    published: str
    published_datetime: datetime = field(
        repr=False, default_factory=lambda: datetime.now()
    )  # this default value may not be the best
    unparsed: Dict = field(
        init=False, repr=False, compare=False, default_factory=dict
    )

    @classmethod
    def from_dict(cls, feed_dict: FeedParserDict):
        #convert to datetime
        feed_dict['published_datetime'] = datetime.fromtimestamp(
            time.mktime(feed_dict['published_parsed']))
        selected_kwargs = {
            key: value
            for key, value in feed_dict.items()
            if key in cls.__match_args__
        }
        _r = cls(**selected_kwargs)
        _r.unparsed = feed_dict
        return _r
