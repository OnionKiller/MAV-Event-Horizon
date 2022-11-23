import requests
import feedparser  # type:ignore
from bs4 import BeautifulSoup  # type:ignore


class WebNodeParser:
    @staticmethod
    def str_form_entry(feedEntry: feedparser.FeedParserDict) -> str:
        link = WebNodeParser.parse_node_link(feedEntry)
        webNode = WebNodeParser.get_parsed_webNode(link)
        content = WebNodeParser.get_webNode_content(webNode)
        return " ".join(content.stripped_strings)

    @staticmethod
    def parse_node_link(feedEntry: feedparser.FeedParserDict) -> str:
        if not feedEntry.has_key("link"):
            raise ValueError("Feed entry doesn't have link field.")
        return feedEntry["link"]

    @staticmethod
    def get_parsed_webNode(pageLink: str) -> BeautifulSoup:
        res = requests.get(pageLink)
        if res.status_code != requests.codes.OK:
            res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser")

    @staticmethod
    def get_webNode_content(pageSoup: BeautifulSoup):
        content = pageSoup.select(".field-body")
        if len(content) != 1:
            raise ValueError(
                "Parse error when retriving the content from the pageSoup."
            )
        return content[0]
