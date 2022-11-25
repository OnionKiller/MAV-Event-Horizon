import logging
import os, sys

sys.path.append(os.path.dirname(os.path.realpath("../src")))

from time import process_time, sleep
from src.RSS_abstracts.Feed import Feed
from src.feed_handler.csv_storage import csvStorage


if __name__ == "__main__":
    store = csvStorage("first_collection.csv")
    feed = Feed(storage=store, link="https://www.mavcsoport.hu/mavinform/rss.xml")

    logging.basicConfig(filename="feed.log", encoding="utf-8", level=logging.INFO)

    while True:
        start = process_time()
        nw = feed.update()
        run_length = process_time() - start
        print(nw)
        for n in nw:
            logging.info(n)
        logging.info(f"feed update run for: {run_length}s")
        # sleep 5 minute
        sleep(60*5)
