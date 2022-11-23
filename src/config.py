import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    BASE_URL = os.environ.get("BASE_URL", "http://localhost.")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self):
        load_dotenv()
