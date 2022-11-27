import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BASE_URL = os.environ.get("BASE_URL", "http://localhost.")
    COGNITIVE_SERVICE_KEY = os.environ.get("COGNITIVE_SERVICE_KEY",None)
    #TODO remove default value
    COGNITIVE_SERVICE_BASE = os.environ.get("COGNITIVE_SERVICE_BASE", "bme-mav-nlp")
    COGNITIVE_SERVICE_ENDPOINT = os.environ.get("COGNITIVE_SERVICE_ENDPOINT","https://"+COGNITIVE_SERVICE_BASE+".cognitiveservices.azure.com/")

    def __init__(self):
        load_dotenv()
