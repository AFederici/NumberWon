from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
import numpy as np

app = Flask(__name__)
ask = Ask(app, '/')

from fanfiction import Fanfiction
from profile_skills import update_current_user

import sys
sys.path.insert(0, 'C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/profiles/Profiles')
from Profile import Profile
from UserDatabase import UserDatabase

alexa_path = 'C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/profiles'
#sys.path.insert(0, alexa_path)
#every Fanfiction instance saves a text file into of top fanfiction for a term
#iterates through all the databases and saves txt files based on preferences
import os
save_path = 'C:/Users/User/Desktop/beaver/NumberWon/numberwon/alexa_skills/fanfiction_files'

for f in os.listdir(alexa_path):
    if f.endswith(".npy"):
        d = UserDatabase(f)
        profiles = [val.pref_dict["fanfiction_pref"] for key, val in d.dict]

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    msg = "Hi. Are you interested in reading some fanfiction made just for you?"
    return question(msg)
@ask.intent("AMAZON.YesIntent")
def yes_intent():
    msg = "Pulling up user preferences for first person in frame, "

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "No problem. Have a nice day."
    return question(msg)

@ask.intent("FanfictionIntent")
def fanfiction_intent():
    u = UserDatabase(np.load('profiles_test_database.npy'))
    listing = [val for key, val in p.pref_dict if key is "#fanfiction pref?"]
    msg = "Pulling up fanfiction about {}".format(", ".join(listing))
    text = f.generate_text("FILL IN HERE")
    return statement(msg) \
        .simple_card(title='CATS says...', content='Make your time')  # edit here
