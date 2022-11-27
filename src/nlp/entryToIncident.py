import nltk
from nltk.corpus import stopwords
from datetime import datetime
import parsedatetime as pdt
from deep_translator import GoogleTranslator
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import spacy

from config import Config


conf = Config()

credential = AzureKeyCredential(conf.COGNITIVE_SERVICE_KEY)
text_analytics_client = TextAnalyticsClient(endpoint=conf.COGNITIVE_SERVICE_ENDPOINT, credential=credential)

def newEntryPipeline(text):
    translatedText = translateText(text)
    keyPhrase_response, entity_response = azureProcess(translatedText)
    nlpDocument = spacyProcess(translatedText)
    line, locations, cause, startDate, endDate = processDocument(keyPhrase_response[0], nlpDocument)
    if cause == None:
        cause = causeFinder(translatedText)
    locations = locationFinder(entity_response)
    if line == None:
        line = "Unknown"
    if len(locations) == 0:
        locations = "Unknown"
    if cause == None or len(cause) == 0:
        cause = "Unknown"
    return line, locations, cause, startDate, endDate

def editEntryPipeline(text, locations, cause, endDate):
    translatedText = translateText(text)
    nlpDocument = spacyProcess(translatedText)
    if cause == "Unknown":
        cause = causeFinder(translatedText)
    endDate = endDateChecker(translatedText, endDate, nlpDocument)
    _, entity_response = azureProcess(translatedText)
    newLocations = locationFinder(entity_response)
    for location in newLocations:
        if location not in locations:
            locations.append(location)
    return locations, cause, endDate

def translateText(text):
    return GoogleTranslator(source='hungarian', target='en').translate(text)

def azureProcess(text):
    document = {}
    document["id"] = "0"
    document["language"] = "en"
    document["text"] = text
    keyPhrase_response = text_analytics_client.extract_key_phrases([document])
    entities_response = text_analytics_client.recognize_entities([document])
    for idx, entity_response in enumerate(entities_response):
        entities_response[idx] = corrigateLocationNames(entity_response, idx)

    return keyPhrase_response, entity_response

def spacyProcess(text):
    nlp = spacy.load("en_core_web_md")
    nlpDocument = nlp(text)
    return nlpDocument

def isLaterDate(date1, date2):
    if int(date1.strftime("%y")) < int(date2.strftime("%y")):
        return True
    if int(date1.strftime("%y")) == int(date2.strftime("%y")):
        if int(date1.strftime("%m")) < int(date2.strftime("%m")):
            return True
        if int(date1.strftime("%m")) == int(date2.strftime("%m")):
            if int(date1.strftime("%d")) < int(date2.strftime("%d")):
                return True
            if int(date1.strftime("%d")) == int(date2.strftime("%d")):
                if int(date1.strftime("%H")) < int(date2.strftime("%H")):
                    return True
    return False

def processDocument(keyPhrases, nlpDocument):
    cal = pdt.Calendar()
    now = datetime.now()

    locations = []
    incidentEndDate = "Unknown"
    endDate = now
    endDateSet = False
    line = None
    cause = None

    for phrase in keyPhrases['key_phrases']:
        if "line" in phrase:
            line = phrase.replace(" line", "")
        if "investigation" in phrase.lower():
            cause = "Accident"
    for entity in nlpDocument.ents:
        if entity.label_ == "DATE" or entity.label_ == "TIME":
            try:
                possibleEndDate = cal.parseDT(entity.text, now)[0]
                if isLaterDate(now, possibleEndDate):
                    if isLaterDate(endDate, possibleEndDate):
                        endDate = possibleEndDate
                        endDateSet = True
            except:
                print("It was an invalid date!")
    if endDateSet:
        incidentEndDate = str(endDate)[:10]
    #Todo: Check possible refactoring of startDate!
    startDate = "Unknown"
    return line, locations, cause, startDate, incidentEndDate

def causeFinder(text):
    stop = set(stopwords.words('english'))
    sentences = nltk.sent_tokenize(text.lower())
    causes = []
    for sentence in sentences:
        if "due to" in sentence:
            allWords = nltk.word_tokenize(sentence)
            words = [word for word in allWords if word not in stop]
            labeledWords = nltk.pos_tag(words)
            keepIt = False
            dueIndex = -1
            for idx, (word,type) in enumerate(labeledWords):
                if word == "due":
                    dueIndex = idx
                    keepIt = True
                if idx > dueIndex and keepIt:
                    if idx == dueIndex+1 and type == "JJ":
                        causes.append(word)
                    else:
                        if type == "NN" or type == "RB":
                            causes.append(word)
                        else:
                            keepIt = False
    sentenceWords = sentence.split(" ")
    if len(causes) == 0:
        for sentenceWord in sentenceWords:
            if "failure" == sentenceWord or "failed" == sentenceWord:
                causes.append("Technical issue")
            if "rain" == sentenceWord or "ice" == sentenceWord or "snow" == sentenceWord:
                causes.append("Weather torubles")
    if len(causes) > 0:
        cause = " ".join(causes)
    else:
        cause = "Unknown"
    return cause

def corrigateLocationNames(entity_response, text):
    specialCharacterDictionary = {}
    specialCharacterDictionary['á'] = ['a']
    specialCharacterDictionary['é'] = ['e']
    specialCharacterDictionary['í'] = ['i']
    specialCharacterDictionary['ó'] = ['o']
    specialCharacterDictionary['ő'] = ['ö']
    specialCharacterDictionary['ú'] = ['u']
    specialCharacterDictionary['ű'] = ['u']

    for entity in entity_response['entities']:
        if entity['category'] == "Location":
            characters = [x for x in entity.text]
            corrected = False
            for idx,char in enumerate(characters):
                if corrected:
                    break
                try:
                    possibleChanges = specialCharacterDictionary[char]
                    for change in possibleChanges:
                        characters = [x for x in entity.text]
                        characters[idx] = change
                        newLocationName = ''.join(characters)
                        if newLocationName.lower() in text.lower():
                            entity.text = newLocationName
                            corrected = True
                except:
                    continue
    return entity_response

def locationFinder(entity_response):
    locations = []
    for entity in entity_response['entities']:
        if entity['category'] == "Location":
            if entity['text'] not in locations and float(entity['confidence_score']) > 0.4:
                locations.append(entity['text'])
    return locations

def endDateChecker(text, incidentEndDate, nlpDocument):
    cal = pdt.Calendar()
    now = datetime.now()
    endDateSet = False
    if "restored" in text and incidentEndDate == "Unknown":
        endDate = now
        for entity in nlpDocument.ents:
            if entity.label_ == "DATE" or entity.label_ == "TIME":
                try:
                    possibleEndDate = cal.parseDT(entity.text, now)[0]
                    if isLaterDate(now, possibleEndDate):
                        if isLaterDate(endDate, possibleEndDate):
                            endDate = possibleEndDate
                            endDateSet = True
                except:
                    print("It was an invalid date!")
    if endDateSet:
        incidentEndDate = str(endDate)[:10]
    if "restored" in text and incidentEndDate == "Unknown":
        incidentEndDate = str(now)[:10]
    return incidentEndDate