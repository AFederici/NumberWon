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

for element in together:
    sys.path.insert(0, save_path)
    fanfiction_dict = f.find_fanfiction(element)
    f.ultimate_function(element, fanfiction_dict)

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
    msg = "Pulling up user preferences for " + session.attributes["Current_User"]
    session.attributes["Current_User"] = session.attributes["Current_User"].lower()

    p = d.dict[session.attributes["Current_User"]]
    listing = [p.find_user_preferences(key) for key, val in p.pref_dict.items() if "fan" in key][0]

    print("preferences: ", listing)
    content = ""
    for term in listing:
        with open("fanfiction_files/" + str(term) + ".txt", "r", 'cp1252') as z:
            t = z.read()
            print("first sentence of files :", t[:30])
            content += term + 'fanfiction: \n' + t + "\n\n"

    return statement(msg) \
        .simple_card(title='Generated FanFic', content=content)

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "No problem. Have a nice day."
    return question(msg)


if __name__ == '__main__':
    app.run(debug=True)
