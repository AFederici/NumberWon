
from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json

#get links off a page: remove all that contain video
#add all the links as pickle files


import sys
sys.path.insert(0, 'C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/search')
from entityDatabase import entityDatabase
edatb = entityDatabase()
edatb.add_Folder_Database('C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/search/pickles')

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
    EntityName = EntityName.lower()
    c = edatb.top_entity_dict(EntityName, most_c=5)
    listing = [tupling[0] for tupling in c]
    return ", ".join(listing)

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
    print(entity, "my entity")
    print(EntTitle, "ÉntTitle")
    if entity is None:
        msg = "No entities found for {}".format(EntTitle)
    msg = "Top entities related to {}: {}".format(EntTitle, entity)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)





























