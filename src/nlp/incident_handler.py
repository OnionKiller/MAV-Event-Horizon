import pandas as pd
import os
from pathlib import Path
from .entryToIncident import editEntryPipeline, newEntryPipeline
from ..RSS_abstracts.RSSEntry import RSSEntry


class IncidentHandler:
    def __init__(self, path):
        self._path = path
        self.__readData(path)

    def handleIncident(self, entry:RSSEntry, text:str):
        try:
            if id in self.incidents.index:
                self.updateIncident(entry.id, entry.published_datetime, text)
            else:
                self.addIncident(entry.id, entry.published_datetime, text)
        except Exception as e: 
            print("Error with handling the incident! Error: ", e)

    def updateIncident(self, id, time, text):
        newLocations, newCause, newEndDate = editEntryPipeline(text, time, self.incidents.loc[id]['Locations'], self.incidents.loc[id]['Cause'], self.incidents.loc[id]['EndDate'])
        change = False
        if newLocations != self.incidents.loc[id]['Locations']:
            self.incidents.loc[id]['Locations'] = newLocations
            change = True
        if self.incidents.loc[id]['Cause'] != newCause:
            self.incidents.loc[id]['Cause'] = newCause
            change = True
        if self.incidents.loc[id]['EndDate'] != newEndDate:
            self.incidents.loc[id]['EndDate'] = newEndDate
            change = True
        if change:
            self.__writeData()
        return
    
    def addIncident(self, id, time, text):
        line, locations, cause, startDate, endDate = newEntryPipeline(text, time)
        newRow = [line, locations, cause, startDate, endDate]
        self.incidents.loc[id] = newRow
        self.__writeData()
        return

    def __readData(self, path):
        if not isinstance(path, Path):
            file_location = Path(path)
        else:
            file_location = path

        if file_location.suffix != ".csv":
            raise ValueError(f"Path {file_location} is not a csv file.")

        if file_location.exists():
            df = pd.read_csv(file_location, index_col="Id")
            self.incidents = df
        else:
            self.incidents = pd.DataFrame(columns=['Id', 'Line', 'Locations', 'Cause', 'StartDate','EndDate'])
            self.incidents = self.incidents.set_index('Id')
    
    def __writeData(self, path):
        self.incidents.to_csv(self._path, index=True)
