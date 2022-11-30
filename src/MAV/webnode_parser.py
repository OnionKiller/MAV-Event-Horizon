import requests
import feedparser  # type:ignore
from bs4 import BeautifulSoup  # type:ignore
from ..RSS_abstracts.RSSEntry import RSSEntry


class WebNodeParser:
    @staticmethod
    def str_form_entry(feed_entry: RSSEntry) -> str:
        webNode = WebNodeParser._get_parsed_webNode(feed_entry.link)
        content = WebNodeParser._get_webNode_content(webNode)
        return " ".join(content.stripped_strings)

    @staticmethod
    def _get_parsed_webNode(page_link: str) -> BeautifulSoup:
        res = requests.get(page_link)
        if res.status_code != requests.codes.OK:
            res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")

    @staticmethod
    def _get_webNode_content(page_soup: BeautifulSoup):
        content = page_soup.select(".field-body")
        if len(content) != 1:
            raise ValueError(
                "Parse error when retriving the content from the pageSoup."
            )
        return content[0]
