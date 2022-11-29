import logging
import os, sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.realpath("../src")))

import pandas as pd

from time import process_time, sleep
from src.RSS_abstracts.Feed import Feed
from src.RSS_abstracts.RSSEntry import RSSEntry
from src.feed_handler.csv_storage import csvStorage
from src.nlp.webnode_parser import WebNodeParser
from src.nlp.incident_handler import IncidentHandler

webpage_log_storage_path = "web_collection.csv"


def fetch_webpage_data(entry: RSSEntry):
    web_node_str = WebNodeParser.str_form_entry(entry)
    df = pd.DataFrame(
        [
            {
                "id": entry.id,
                "link": entry.link,
                "published": entry.published,
                "webpage": web_node_str,
            }
        ]
    )

    if not Path(webpage_log_storage_path).exists():
        df.to_csv(webpage_log_storage_path)
    else:
        df.to_csv(webpage_log_storage_path, mode="a", header=False, index=False)


if __name__ == "__main__":
    store = csvStorage("first_collection.csv")
    incident_handler = IncidentHandler()

    feed = Feed(storage=store, link="https://www.mavcsoport.hu/mavinform/rss.xml")

    logging.basicConfig(filename="feed.log", encoding="utf-8", level=logging.INFO)

    while True:
        start = process_time()
        nw = feed.update()
        run_length = process_time() - start
        start = process_time()
        for n in nw:
            print("New entry: ", n)
            logging.info(n)
            web_text = WebNodeParser.str_form_entry(n)
            incident_handler.handleIncident(n, web_text)
        processing_length = process_time() - start

        logging.info(f"feed update run for: {run_length}s")
        logging.info(f"update processing run for: {processing_length}s")

        # dump incident dataframe
        # TODO proper incident handling
        incident_handler.incidents.to_csv("incident_collection.csv")

        # sleep 5 minute
        sleep(60 * 5)
