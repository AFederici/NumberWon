from flask import Flask
from flask_ask import Ask, statement, question, session
from face.FaceRec import Face_Recognition
from face.database import Database
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase, UserDatabaseNames
import numpy as np

f = Face_Recognition()
d = Database()
ud = UserDatabase()
"""load a file of users and databases somewhere else"""
m = Profile("Megan")

app = Flask(__name__)
ask = Ask(app, '/')

@app.route('/')
def homepage():
    return "Profiles?"

@ask.launch
def start_skill():
    #put these things at beginning where it just loads in already-created database and then assigns session att to the list
    ud.update(m.get_name(), m)
    #udn = UserDatabaseNames(ud)
    session.attributes["User_Profiles"] = ud.names()
    current_user = ""
    for i in session.attributes["User_Profiles"]:
        if ud.dict[i].profile_status:
            current_user = i
            #print("current user is " + str(i))
    msg = "The current User is {}.".format(current_user)
    #print(msg)
    return statement(msg)

'''Adding attributes/ to current profile'''
#preferences: stories, news, music, stocks

'''Switching profiles. (for now, based on img. Later will be based on voice) (New profiles have to be added manually?'''

'''Adding a new profile. (Name [amazon american names], Picture/voice sample, any preferences [amazon literals])'''

if __name__ == '__main__':
    app.run(debug=True)