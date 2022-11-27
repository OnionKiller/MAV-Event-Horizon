import nltk
from nltk.corpus import stopwords
from datetime import datetime
import parsedatetime as pdt
from deep_translator import GoogleTranslator
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os
import spacy
from spacy.matcher import Matcher
from datetime import datetime
from time import mktime

credential = AzureKeyCredential(os.getenv('COGNITIVE_SERVICE_KEY'))
text_analytics_client = TextAnalyticsClient(endpoint="https://bme-mav-nlp.cognitiveservices.azure.com/", credential=credential)

nlp = spacy.load("en_core_web_md")
cal = pdt.Calendar()

def newEntryPipeline(text, time):
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
    startDate = convertEntryTime(time)
    return line, locations, cause, startDate, endDate

def editEntryPipeline(text, time, locations, cause, endDate):
    translatedText = translateText(text)
    nlpDocument = spacyProcess(translatedText)
    if cause == "Unknown":
        cause = causeFinder(translatedText)
    endDate = endDateChecker(translatedText, time, endDate, nlpDocument)
    _, entity_response = azureProcess(translatedText)
    newLocations = locationFinder(entity_response)
    for location in newLocations:
        if location not in locations:
            locations.append(location)
    return locations, cause, endDate

def convertEntryTime(time):
    dt = datetime.fromtimestamp(mktime(time))
    return str(dt)[:10]

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
    startDate = "Unknown"
    return line, locations, cause, startDate, incidentEndDate

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

def endDateChecker(text, time, incidentEndDate, nlpDocument):
    now = datetime.now()
    stop = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stop]
    text2 = ' '.join(words)

    indicatorWords = ['resolved', 'fixed', 'restored']
    pattern = [[{'LOWER': {"IN": indicatorWords}}]]
    matcher = Matcher(nlp.vocab)
    matcher.add("ENDING", pattern)
    doc = nlp(text2)
    matches = matcher(doc)

    if len(matches) > 0:
        endDateSet = False
        if incidentEndDate == "Unknown":
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
    if len(matches) > 0 and incidentEndDate == "Unknown":
        incidentEndDate = convertEntryTime(time)
    return incidentEndDate

def causeFinder(text):
    stop = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in stop]
    text = ' '.join(words)

    weatherLemmas = ['rain', 'snow', 'ice']
    pattern1 = [[{"LOWER": "due"}, {"POS": "ADJ", "OP": "?"}, {"POS": "NOUN", "OP": "+"}]]
    pattern2 = [[{"LEMMA": {"IN": weatherLemmas}}]]
    pattern3 = [[{"LOWER": "investigation"}], [{"LOWER": "ran"}, {"LOWER": "over"}], [{"LOWER": "crashed"}]]

    matcher = Matcher(nlp.vocab)
    matcher.add("DueCause", pattern1, greedy="LONGEST")
    matcher.add("WeatherCause", pattern2)
    matcher.add("AccidentCause", pattern3)

    doc = nlp(text)
    matches = matcher(doc)
    cause = "Unknown"
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        
        match string_id:
            case "DueCause":
                cause = doc[start+1:end].text
            case "WeatherCause":
                cause = "Weather caused issues"
            case "AccidentCause":
                cause = "Accident"
            case _:
                cause ="Unknown"
    return cause