import click
import logging
import pandas as pd

from .config import Config
from ..RSS_abstracts.Feed import Feed
from ..feed_handler.csv_storage import csvStorage
from ..nlp.webnode_parser import WebNodeParser
from ..nlp.incident_handler import IncidentHandler
from time import process_time, sleep

conf = Config()


@click.group()
def cli():
    pass


def sync_incident_handler(handler: IncidentHandler, sanitize_duplicates: bool = True):
    """IO intensive data syncronisation

    Params:
    -------
    handler: IncidentHandler
        Incident handler class instance
    sanitize_duplicates:bool=True
        If there are duplicates, remove them. Useful, if for some reason there are data duplication.
    """
    df: pd.DataFrame = handler.incidents
    saved_df = pd.DataFrame()
    if df.empty:
        return
    if conf.INCIDENTS_STORAGE_LOCATION.exists():
        saved_df = pd.read_csv(
            conf.INCIDENTS_STORAGE_LOCATION, parse_dates=["StartDate", "EndDate"]
        )
    merged = pd.concat([df, saved_df])
    if sanitize_duplicates:
        # if for some reason duplicates are observed, drop them
        merged = merged.drop_duplicates()
    merged.to_csv(conf.INCIDENTS_STORAGE_LOCATION, index=False)


def single_scrape_iteration(feed, incident_handler):
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

    # TODO proper save mechanism for incident handling
    sync_incident_handler(incident_handler,False)


@click.command()
@click.option(
    "--sleep_time",
    prompt="Sleep time in seconds. ",
    help="Sleep time in seconds. It is blocking for Python. Use it with care.",
    # sleep 5 minute
    default=60 * 5,
)
def main_scrape_loop(sleep_time: int):
    """Program, to run indefinetly, periodically checking an RSS feed, and flushing data to csv file."""
    store = csvStorage(conf.RSS_FEED_STORAGE_LOCATION)
    incident_handler = IncidentHandler()

    feed = Feed(storage=store, link="https://www.mavcsoport.hu/mavinform/rss.xml")

    logging.basicConfig(
        filename=conf.FEED_LOG_LOCATION, encoding="utf-8", level=logging.INFO
    )
    click.echo('Start listening.')
    while True:
        single_scrape_iteration(feed, incident_handler)
        sleep(sleep_time)


cli.add_command(main_scrape_loop)
