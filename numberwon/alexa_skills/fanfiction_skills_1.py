from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
import numpy as np
import html2text

app = Flask(__name__)
ask = Ask(app, '/')

from fanfiction import Fanfiction
from profile_skills import update_current_user
import itertools

from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase

f = Fanfiction()
d = UserDatabase("profiles/profiles_test_database.npy")

together = list()
#find all keys that have fan in them
profiles = [val.find_user_preferences(key) for key, val in d.dict.items() if "fan" in val.pref_dict]
together.extend(itertools.chain.from_iterable(profiles))
#together is a list with all the possible fanfiction preferences: NO elements should be "None"

#MEGAN PLEASE DEFIND SAVE_PATH as '.../NumberWon/numberwon/alexa_skills/fanfiction_files
save_path = #MEGAN INSERT HERE

import sys
for element in together:
    sys.path.insert(0, save_path)
    fanfiction_dict = f.find_fanfiction(element)
    a = open(element + '.txt', 'w')
    a.write(fanfiction_dict[element])
    a.close()

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "I could not find a user I recognize."
        return statement(msg)
    else:
        msg = "Hi" + session.attributes["Current_User"] + ". Are you interested in reading some fanfiction made just for you?"
    print("current user: ", session.attributes["Current_User"])
    return question(msg)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    msg = "Ok " + session.attributes["Current_User"] +  ". How many characters of fanfiction would you like to generate for each topic?"
    return question(msg)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "No problem. Have a nice day."
    return question(msg)

@ask.intent("CharacterIntent")
def char_intent(number): #number type: AMAZON.NUMBER
    session.attributes["Current_User"] = session.attributes["Current_User"].lower()
    p = d.dict[session.attributes["Current_User"]]
    listing = tuple(p.get_preferences_by_user(session.attributes["Current_User"], key) for key, val in p.pref_dict if "fan" in key)

    print("preferences: ", listing)
    content = ""

    for term in listing:
        with open(term + ".txt", "r") as z:
            value = str(z.read())
            lm = f.train_lm(value, 13)
            text = html2text.html2text(f.generate_text(lm, 13, number))
            text = text[:text.rfind(".") + 1]
            content += term.title() + 'Fanfiction: \n' + value + "\n\n"

    msg = "Pulling up fanfiction for " + session.attributes["Current_User"]
    return statement(msg).simple_card(title='Generated FanFic', content=content)

if __name__ == '__main__':
    app.run(debug=True)
