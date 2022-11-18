
from dataclasses import dataclass, field
from typing import Dict, List
from feedparser import FeedParserDict


@dataclass
class RSSEntry(object):
    id: int
    title: str
    link: str
    published: str
    published_parsed: List[int] = field(
        default_factory=list)  # type may not be this exact one
    unparsed: Dict = field(init=False, compare=False, default_factory=dict)

    @classmethod
    def from_dict(cls, feed_dict: FeedParserDict):
        selected_kwargs = {
            key: value for key, value in feed_dict.items() if key in cls.__annotations__}
        _r = cls(**selected_kwargs)
        _r.unparsed = feed_dict
        return _r
