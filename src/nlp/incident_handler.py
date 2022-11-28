import pandas as pd
from .entryToIncident import *

class IncidentHandler:
    def __init__(self):
        self.incidents = pd.DataFrame(columns=['Id', 'Line', 'Locations', 'Cause', 'StartDate','EndDate'])
        self.incidents = self.incidents.set_index('Id')

    #Todo: RSSentryt és a textet itt megkapni
    def handleIncident(self, id, text):
        try:
            if id in self.incidents.index:
                self.updateIncident(id, text)
            else:
                self.addIncident(id, text)
        except Exception as e: 
            print(e)
            print("Error with handling the incident!")

    def updateIncident(self, id, text):
        newLocations, newCause, newEndDate = editEntryPipeline(text, self.incidents.loc[id]['Locations'], self.incidents.loc[id]['Cause'], self.incidents.loc[id]['EndDate'])
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
    
    def addIncident(self, id, text):
        line, locations, cause, startDate, endDate = newEntryPipeline(text)
        newRow = [line, locations, cause, startDate, endDate]
        self.incidents.loc[id] = newRow
        return

def main():
    incidentHandler = IncidentHandler()
    incidentHandler.handleIncident("31", "A Budapest-Szolnok-Békéscsaba-Lőkösháza vonalon december 10-ig pályakarbantartási munkák miatt a vonatok módosított menetrend szerint közlekednek.\
 A Lőkösházáról a Keleti pályaudvarra 6:40-kor induló 759-es számú Békés InterCity helyett Lőkösháza és Békéscsaba között, a délutáni Lőkösháza-Kétegyháza,\
 illetve a Kétegyháza-Lőkösháza viszonylatú személyvonatok (7544, 7546, 7545, 7543, 7553) helyett teljes útvonalon pótlóbuszok közlekednek.\
 A 346-os és 347-es számú Dacia nemzetközi vonat módosított menetrend szerint Biharkeresztesen át - kerülő úton közlekedik a Corvin nemzetközi vonatokkal egyesítve.")
    incidentHandler.handleIncident("21", "Műszaki ok miatt a Debrecenből Tiszafüredre 22:45-kor induló pótlóbusz a teljes útvonalon közlekedik. Emiatt a november 26-án, szombaton a Tiszafüredről Balmazújvárosra 4:46-kor induló vonat nem közlekedik, helyette pótlóbusz szállítja az utasokat.")
    incidentHandler.handleIncident("23", "Budapest! Helyszínelnek a hatóságok.")
    incidentHandler.handleIncident("23", "Track conditions are good.")
    print(incidentHandler.incidents)

if __name__ == "__main__":
    main()
