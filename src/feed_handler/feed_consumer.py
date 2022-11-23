import feedparser  # type:ignore


class FeedConsumer:
    _feed_url: str
    _etag: str
    _last_known: feedparser.FeedParserDict

    def __init__(self, url=r"https://www.mavcsoport.hu/mavinform/rss.xml"):
        self._feed_url = url
        self._etag = None

    def fetch(self):
        new_feed_state = feedparser.parse(
            r"https://www.mavcsoport.hu/mavinform/rss.xml", etag=self._etag
        )
        if new_feed_state.status == 304:
            # TODO log too frequent refresh
            return self._last_known
        if new_feed_state.status != 200:
            raise NotImplementedError("Handle if feed is down!")
        self._last_known = new_feed_state
        self._etag = self._last_known.etag
        return self._last_known
