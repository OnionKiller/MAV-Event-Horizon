from dataclasses import dataclass, field
import time
from typing import Dict
from feedparser import FeedParserDict


@dataclass(match_args=True)
class RSSEntry(object):
    id: int
    title: str
    link: str
    published: str
    published_parsed: time.struct_time = field(
        repr=False, default_factory=time.struct_time
    )  # type may not be this exact one
    unparsed: Dict = field(
        init=False, repr=False, compare=False, default_factory=dict
    )

    @classmethod
    def from_dict(cls, feed_dict: FeedParserDict):
        selected_kwargs = {
            key: value
            for key, value in feed_dict.items()
            if key in cls.__match_args__
        }
        _r = cls(**selected_kwargs)
        _r.unparsed = feed_dict
        return _r
