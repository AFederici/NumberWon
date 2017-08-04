from flask import Flask
from flask_ask import Ask, statement, session, question
import requests
import time
import unidecode
import json
from search.entityDatabase import entityDatabase
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase
from face.FaceRec import Face_Recognition
from face.database import Database
from profile_skills import update_current_user

edatb = entityDatabase()
ud = UserDatabase("profiles/profiles_test_database.npy")
edatb.add_Folder_Database("search/pickles")

#import all the shit
#when start skill, sees if current user is someone it recognizes. If yes, calls something else.
    #can check if session.attributes[current_user] == none or not
#if no, proceede as normal
#if yes, only check certain documents

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Hello"

@ask.launch
def start_skill():
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "Hello. What would you like to hear about the news?"
        return question(msg)
    else:
        pref = ud.get_preferences_by_user(session.attributes["Current_User"], "news")
        msg = "Tops news based on your preferences "
        for i in pref:
            headline  = get_headlines(i)
            if headline is None:
                continue
            else:
                msg += str(i) + ": " + str(headline) + " ."
        return statement(msg)
    

def get_headlines(NewsTitle):
    return edatb.docsearch(NewsTitle)

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    return question("What would you like to know more about?")

@ask.intent("AMAZON.NoIntent")
def no_intent():
    msg = "Ok, thanks. Have a nice day."
    return statement(msg)

@ask.intent("NewsIntent")
def news_intent(NewsTitle):
    headline  = get_headlines(NewsTitle)
    msg = "Tops news on {}: {}".format(NewsTitle,headline)
    if headline is None:
        msg = "No news was found for {}".format(NewsTitle)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
