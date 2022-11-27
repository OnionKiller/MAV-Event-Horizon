import pandas as pd
from entryToIncident import *


class IncidentHandler:
    def __init__(self):
        self.incidents = pd.DataFrame(columns=['Id', 'Line', 'Locations', 'Cause', 'StartDate','EndDate'])
        self.incidents = self.incidents.set_index('Id')

    def handleIncident(self, entry, text):
        try:
            if id in self.incidents.index:
                self.updateIncident(entry.id, entry.published_datetime, text)
            else:
                self.addIncident(entry.id, entry.published_datetime, text)
        except Exception as e: 
            print(e)
            print("Error with handling the incident!")

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
        return change
    
    def addIncident(self, id, time, text):
        line, locations, cause, startDate, endDate = newEntryPipeline(text, time)
        newRow = [line, locations, cause, startDate, endDate]
        self.incidents.loc[id] = newRow
        return