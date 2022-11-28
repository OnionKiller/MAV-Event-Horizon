# MAV-Event-Horizon
BME Software Architectures assignment in 2022. It scrapes MÁV RSS feed, and analyses data with NLP.

# Install

To install the sotware you have to first set the enviroment variables in either the  `.env` file, or in your operating system.
The enviroment variables the program expects are:
* `COGNITIVE_SERVICE_KEY`: this is required, it is an Azure API key
* `COGNITIVE_SERVICE_BASE` default='bme-mav-nlp': this is the API endpoint name to use, it is automaticly appended to the full link.
* `COGNITIVE_SERVICE_ENDPOINT` default='https://`COGNITIVE_SERVICE_BASE`.cognitiveservices.azure.com/': this is the actual endpoint to use for Azure NLP
* `RSS_FEED_STORAGE_LOCATION` default='rss_feed_collection.csv': where data from the RSS feed are stored
* `INCIDENTS_STORAGE_LOCATION` default='incidents.csv': where NLP results are stored
* `INCIDENTS_STORAGE_LOCATION` default='feed.log': incident storage creates logs, which are stored here 

The package requires Python 3.10 or later.

To install the packages simply run:
```bash
pip install -r requirements.txt
```

# Run

To run the main loop there is a cli interface:

```bash
python -m scr <seconds>
```
where the parameter determines how much time should be between RSS fetches.



# Setup
This repository uses `pip-tools`. 
To set up a development enviroment run:
```bash
pip install -r dev-requirements.txt
```
To update the requirements of the proejct, modify the correct `*requirements.in` file, and the run:
```bash
pip-compile requirements.in --upgrade --resolver=backtracking
```
To upgrade your virtual enviroment run:
```bash
pip-sync
```
To set up production use the `requirements.txt`.
