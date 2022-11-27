import os
from pathlib import Path

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BASE_URL = os.environ.get("BASE_URL", "http://localhost.")
    
    #azure api keys
    COGNITIVE_SERVICE_KEY = os.environ.get("COGNITIVE_SERVICE_KEY",None)
    #TODO remove default value
    COGNITIVE_SERVICE_BASE = os.environ.get("COGNITIVE_SERVICE_BASE", "bme-mav-nlp")
    COGNITIVE_SERVICE_ENDPOINT = os.environ.get("COGNITIVE_SERVICE_ENDPOINT","https://"+COGNITIVE_SERVICE_BASE+".cognitiveservices.azure.com/")

    #csv storage locations
    RSS_FEED_STORAGE_LOCATION = Path(os.environ.get("RSS_FEED_STORAGE_LOCATION","rss_feed_collection.csv"))

    INCIDENTS_STORAGE_LOCATION = Path(os.environ.get("INCIDENTS_STORAGE_LOCATION","incidents.csv"))

    FEED_LOG_LOCATION = Path(os.environ.get("INCIDENTS_STORAGE_LOCATION","feed.log"))

    def __init__(self):
        load_dotenv()
