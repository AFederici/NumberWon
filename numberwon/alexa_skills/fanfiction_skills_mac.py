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

from fanfiction_files.fanfiction import Fanfiction
from profile_skills import update_current_user
import itertools

from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase

f = Fanfiction()
d = UserDatabase("profiles/profiles_test_database.npy")

save_path = "/Users/megankaye/Desktop/BeaverWorks/Work/NumberWon/numberwon/alexa_skills/fanfiction_files"
together = list()
#find all keys that have fan in them
profiles = [val.find_user_preferences(key) for key, val in d.dict.items() if "fan" in val.pref_dict]
together.extend(itertools.chain.from_iterable(profiles))
#together is a list with all the possible fanfiction preferences: NO elements should be "None"

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
        msg = "Hi " + session.attributes["Current_User"] + ". Are you interested in reading some fanfiction made just for you?"
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
    listing = [val2 for key1, val2 in p.pref_dict.items() if "fan" in key1]
    listing = itertools.chain.from_iterable(listing)
    print("preferences: ", listing)
    content = ""

    for term in listing:
        with open("fanfiction_files/" + str(term) + ".txt", "r", encoding='cp1252') as z:
            value = str(z.read())
            lm = f.train_lm(value, 13)
            text = html2text.html2text(f.generate_text(lm, 13, int(number)))
            text = text[:text.rfind(".") + 1]
            content += term.title() + ' Fanfiction: \n' + text + "\n\n"

    msg = "Pulling up fanfiction for " + session.attributes["Current_User"]
    return statement(msg).simple_card(title='Generated FanFic', content=content)

if __name__ == '__main__':
    app.run(debug=True)
