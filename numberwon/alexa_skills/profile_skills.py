from flask import Flask
from flask_ask import Ask, statement, question, session
from face.FaceRec import Face_Recognition
from face.database import Database
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase
import numpy as np

f = Face_Recognition()
ud = UserDatabase("profiles_test_database.npy")

app = Flask(__name__)
ask = Ask(app, '/')

current_user = None
checking_user = 0
adding_user = 0
temp_name = ""

@app.route('/')
def homepage():
    return "Profiles?"

@ask.launch
def start_skill():
    session.attributes["User_Profiles"] = ud.names()
    for i in session.attributes["User_Profiles"]:
        if ud.dict[i].profile_status:
            global current_user
            current_user = i
    if current_user is None:
        msg = "The current user is no one"
    else:
        #if current profile is still nothing, calls check_user_profile. If profile unknown, goes to dummy profile.
        msg = "The current user is {}.".format(current_user)
    return statement(msg)


'''Adding attributes/ to current profile'''

@ask.intent("GetPreferenceIntent")
def get_pref_intent(preferenceslot):
    global current_user
    #pref = " ".join(ud.get_preferences_by_user(current_user, preferenceslot))
    if current_user is None:
        msg = "There is no current user saved."
    else:
        msg = "Your preferences for {} are {}".format(preferenceslot, ud.get_preferences_by_user(current_user, preferenceslot))
    return statement(msg)

@ask.intent("AddPreferenceIntent")
def add_pref_intent(preferenceslot, addingpreferenceslot):
    global current_user
    if current_user is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(current_user, preferenceslot, addingpreferenceslot)
        msg = "Your preferences for {} are now {}".format(preferenceslot, ud.get_preferences_by_user(current_user, preferenceslot))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
    return statement(msg)

@ask.intent("RemovePreferenceIntent")
def add_pref_intent(preferenceslot, removingpreferenceslot):
    global current_user
    if current_user is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(current_user, preferenceslot, removingpreferenceslot)
        msg = "Your preferences for {} are now {}".format(preferenceslot, ud.get_preferences_by_user(current_user, preferenceslot))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
    return statement(msg)

'''Switching profiles. (for now, based on img. Later will be based on voice)'''

def update_current_user():
    #takes a picture/takes voice sample
    #matches it to database
    #returns either the current user or "user could not be found"
    '''can be called in the background of some functions!!!'''
    desc = f.get_face_descriptor_vector()
    user = ud.compare_faces(desc)
    global current_user
    if not current_user is None:
        ud.get_user_by_name(current_user).profile_status = False
        #print(str(current_user) + " is now " + str(ud.get_user_by_name(current_user).profile_status))
    current_user = user
    if not current_user is None:
        ud.get_user_by_name(current_user).profile_status = True
        #print(str(current_user) + " is now " + str(ud.get_user_by_name(current_user).profile_status))

@ask.intent("CurrentUserIntent")
def check_user():
    #updates user based off of user command
    #calls update_current_user
    #if user could not be found, asks if that is correct.
    #If yes, user becomes a dummy profile and user is prompted if they want to add a profile. 
    #If no, user face vectors are updated based on the correct profile
    global current_user
    global checking_user
    if current_user is None:
        msg = "I could not see anyone I identify. Would you like me to add a user?"
        checking_user = 1
    else:
        msg = "The current user is {}. Is this the correct user?".format(current_user) 
        checking_user = 2
    return question(msg)

@ask.intent("YesIntent")
def yes_intent():
    global checking_user
    global adding_user
    global temp_name
    if checking_user == 1:
        msg = "Please say the name of the user."
        checking_user = 3
        return question(msg)
    if checking_user == 2:
        msg = "Great. Thank you."
        checking_user = 0
        return statement(msg)
    if checking_user == 4:
        msg = "The user has been added."
        checking_user = 0
        ud.update(temp_name, Profile(temp_name, f.get_face_descriptor_vector()))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
        current_user = temp_name
        return statement(msg)
    if adding_user == 2:
        msg = "The user has been added."
        adding_user = 0
        ud.update(temp_name, Profile(temp_name, f.get_face_descriptor_vector()))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
        current_user = temp_name
        return statement(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

@ask.intent("NoIntent")
def no_intent():
    global checking_user
    global adding_user
    if checking_user == 1 and adding_user == 0:
        msg = "Alright. Thank you."
        current_user = None
        checking_user = 0
        return statement(msg)
    if checking_user == 2 and adding_user == 0:
        msg = "My apologies. Please try again."
        checking_user = 0
        return statement(msg)
    if checking_user == 4 and adding_user == 0:
        msg = "My apologies. Please say the name again."
        checking_user = 3
        return question(msg)
    if adding_user == 2 and checking_user == 0:
        adding_user = 1
        msg = "My apologies. Please say the name again."
        return question(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

@ask.intent("NameIntent")
def name_intent(nameslot):
    global checking_user
    global adding_user
    global temp_name
    if checking_user == 3 and adding_user == 0:
        checking_user = 4
        temp_name = nameslot
        msg = "Is {} correct?".format(nameslot)
        return question(msg)
    if adding_user == 1 and checking_user == 0:
        adding_user = 2
        temp_name = nameslot
        msg = "Is {} correct?".format(nameslot)
        return question(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

'''Adding a new profile. (Name [amazon american names], Picture/voice sample [taken right there], any preferences [amazon literals])'''

@ask.intent("AddUserIntent")
def add_user_intent():
    global adding_user
    if adding_user == 0 and checking_user == 0:
        checking_user = 0
        msg = "Please say the name of the user you would like to add."
        adding_user = 1
        return question(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)