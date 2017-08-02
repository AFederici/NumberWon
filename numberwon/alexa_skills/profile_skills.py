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

del_user = False
checking_user = 0
adding_user = 0
temp_name = ""

@app.route('/')
def homepage():
    return "Profiles?"

@ask.launch
def start_skill():
    session.attributes["User_Profiles"] = ud.names()
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    session.attributes["Current_User"]
    if session.attributes["Current_User"] is None:
        msg = "The current user is no one"
    else:
        msg = "The current user is {}.".format(session.attributes["Current_User"])
    return question(msg)

'''Adding attributes/ to current profile'''

@ask.intent("GetPreferenceIntent")
def get_pref_intent(preferenceslot):
    #pref = " ".join(ud.get_preferences_by_user(current_user, preferenceslot))
    if session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        msg = "Your preferences for {} are {}".format(preferenceslot, ud.get_preferences_by_user(session.attributes["Current_User"], preferenceslot))
    return statement(msg)

@ask.intent("AddPreferenceIntent")
def add_pref_intent(preferenceslot, addingpreferenceslot):
    if session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], preferenceslot, addingpreferenceslot)
        msg = "Your preferences for {} are now {}".format(preferenceslot, ud.get_preferences_by_user(session.attributes["Current_User"], preferenceslot))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
    return statement(msg)

@ask.intent("RemovePreferenceIntent")
def add_pref_intent(preferenceslot, removingpreferenceslot):
    if session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], preferenceslot, removingpreferenceslot)
        msg = "Your preferences for {} are now {}".format(preferenceslot, ud.get_preferences_by_user(session.attributes["Current_User"], preferenceslot))
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
    session.attributes["Current_User"] = user

@ask.intent("CurrentUserIntent")
def check_user():
    #updates user based off of user command
    #calls update_current_user
    #if user could not be found, asks if that is correct.
    #If yes, user becomes a dummy profile and user is prompted if they want to add a profile. 
    #If no, user face vectors are updated based on the correct profile
    global checking_user
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "I could not see anyone I identify. Would you like me to add a user?"
        checking_user = 1
    else:
        msg = "The current user is {}. Is this the correct user?".format(session.attributes["Current_User"]) 
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
        session.attributes["Current_User"] = temp_name
        temp_name = ""
        return statement(msg)
    if adding_user == 2:
        msg = "The user has been added."
        adding_user = 0
        ud.update(temp_name, Profile(temp_name, f.get_face_descriptor_vector()))
        ud.save_obj("profiles_test_database.npy")
        session.attributes["User_Profiles"] = ud.names()
        session.attributes["Current_User"] = temp_name
        temp_name = ""
        return statement(msg)
    if del_user == True and adding_user == 0 and checking_user == 0:
        msg = "The user has been deleted."
        if session.attributes["Current_User"] == temp_name:
            session.attributes["Current_User"] = None
        if temp_name in ud.list_of_names:
            ud.list_of_names.remove(temp_name)
        if temp_name in ud.dict:
            del ud.dict[temp_name]
        session.attributes["User_Profiles"] = ud.names()
        del_user = False
        temp_name = ""
        return statement(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

@ask.intent("NoIntent")
def no_intent():
    global checking_user
    global adding_user
    global del_user
    if checking_user == 1 and adding_user == 0:
        msg = "Alright. Thank you."
        session.attributes["Current_User"] = None
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
    if del_user == True and adding_user == 0 and checking_user == 0:
        msg = "Alright."
        del_user = False
        return statement(msg)
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

''' Deleting a profile '''

@ask.intent("RemoveUserIntent")
def rem_user_intent(remnameslot):
    msg = "Are you sure you would like to delete {} from users?".format(remnameslot)
    global del_user
    global temp_name
    temp_name = remnameslot
    del_user = True
    return question(msg)


'''Retake photo of current user!!/switch users verbally/retake photo of user verbally'''


if __name__ == '__main__':
    app.run(debug=True)