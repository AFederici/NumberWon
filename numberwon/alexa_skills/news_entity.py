
from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
from search.entityDatabase import entityDatabase

edatb = entityDatabase()
edatb.add_Folder_Database(self, "C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/pickles")
#get links off a page: remove all that contain video
#add all the links as pickle files
app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hello. Would you like to hear top entities corresponding to a search term?"
    return question(msg)

def get_entity(EntityName):
    return edatb.top_entity_dict(self, EntityName, most_c=10)

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    msg = "What would you like to hear more about?"
    return question(msg)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

@ask.intent("EntIntent")
def ent_intent(EntTitle):
    entity = get_entity(EntTitle)
    msg = "Tops news on {}: {}".format(NewsTitle,headline)
    if headline is None:
        msg = "No news was found for {}".format(NewsTitle)
    return statement(msg)