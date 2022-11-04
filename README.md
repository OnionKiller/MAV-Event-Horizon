# MAV-Event-Horizon
BME Software Architectures assignment in 2022. It scrapes MÁV RSS feed, and analyses data with NLP.

# Setup
This repository uses `pip-tools`. 
To set up a development enviroment run:
```bash
pip install -r dev-requirements.txt
```
To update the requirements of the proejct, modify the correct `*requirements.in` file, and the run:
```bash
pip-compile requirements.in --upgrade
```
To upgrade your virtual enviroment run:
```bash
pip-sync
```
To set up production use the `requirements.txt`.
