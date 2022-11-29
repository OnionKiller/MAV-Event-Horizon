import os
from pathlib import Path

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    def __init__(self):
        load_dotenv()
        self.BASE_URL = os.environ.get("BASE_URL", "http://localhost.")

        # azure api keys
        self.COGNITIVE_SERVICE_KEY = os.environ.get("COGNITIVE_SERVICE_KEY", None)
        # TODO remove default value
        self.COGNITIVE_SERVICE_ENDPOINT = os.environ.get(
            "COGNITIVE_SERVICE_ENDPOINT",
            "https://bme-mav-nlp.cognitiveservices.azure.com/",
        )

        # csv storage locations
        self.RSS_FEED_STORAGE_LOCATION = Path(
            os.environ.get("RSS_FEED_STORAGE_LOCATION", "rss_feed_collection.csv")
        )

        self.INCIDENTS_STORAGE_LOCATION = Path(
            os.environ.get("INCIDENTS_STORAGE_LOCATION", "incidents.csv")
        )

        self.FEED_LOG_LOCATION = Path(
            os.environ.get("INCIDENTS_STORAGE_LOCATION", "feed.log")
        )
