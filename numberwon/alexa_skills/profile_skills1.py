from flask import Flask
from flask_ask import Ask, statement, question, session
from face.FaceRec import Face_Recognition
from face.database import Database
from profiles.Profiles.Profile import Profile
from profiles.Profiles.UserDatabase import UserDatabase
import numpy as np
#from vrecog.record import record_to_file
#import vrecog.speaker_classifier_tflearn as speaker_classifier_tflearn


f = Face_Recognition()
ud = UserDatabase("profiles/profiles_test_database.npy")

app = Flask(__name__)
ask = Ask(app, '/')

del_user = False
checking_user = 0
adding_user = 0
temp_name = ""
temp_face_vectors = 0

@app.route('/')
def homepage():
    return "Profiles?"

@ask.launch
def start_skill():
    """ Starts the skill. Updates current user and if it doesn't exist assigns it to None. """
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "The current user is no one"
    else:
        msg = "The current user is {}.".format(session.attributes["Current_User"])
    return question(msg)


'''Adding attributes/ to current profile'''

@ask.intent("GetPreferenceIntent")
def get_pref_intent(categoryslot):
    """ returns the preferences saved based on the user
        if there are no preferences, it returns something None.
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL """
    
    if categoryslot == "":
        msg = "I could not find that preference. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    elif ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot) is None:
        msg = "You have no preferences for {} saved.".format(categoryslot)
    else:
        msg = "Your preferences for {} are {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
    return statement(msg)

@ask.intent("AddPreferenceIntent")
def add_pref_intent(categoryslot, preferenceslot):
    """ adds a preference to the Profile object!
    
        Parameters
        ----------
        preferenceslot : an AMAZON.LITERAL 
        categoryslot : an AMAZON.LITERAL"""
    if categoryslot == "" or preferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], categoryslot, preferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("AddPreferenceStockIntent")
def add_pref_intent(categoryslot, stockpreferenceslot):
    """ adds a preference to the Profile object!
    
        Parameters
        ----------
        stockpreferenceslot : a custom list of stocks 
        categoryslot : an AMAZON.LITERAL """
    
    if categoryslot == "" or stockpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], "stocks", stockpreferenceslot)
        msg = "Your preferences for {} are now {}".format("stocks", ud.get_preferences_by_user(session.attributes["Current_User"], "stocks"))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("AddPreferenceBookIntent")
def add_pref_intent(categoryslot, bookpreferenceslot):
    """ adds a preference to the Profile object!
    
        Parameters
        ----------
        bookpreferenceslot : an AMAZON.LITERAL 
        categoryslot : an AMAZON.LITERAL """
    
    if categoryslot == "" or bookpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], categoryslot, bookpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("AddPreferenceCharIntent")
def add_pref_intent(categoryslot, charpreferenceslot):
    """ adds a preference to the Profile object!
    
        Parameters
        ----------
        charpreferenceslot : an AMAZON.LITERAL 
        categoryslot : an AMAZON.LITERAL """
    
    if categoryslot == "" or charpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], categoryslot, charpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("AddPreferenceTVIntent")
def add_pref_intent(categoryslot, TVpreferenceslot):
    """ adds a preference to the Profile object!
    
        Parameters
        ----------
        TVpreferenceslot : an AMAZON.LITERAL 
        categoryslot : an AMAZON.LITERAL"""
    if categoryslot == "" or TVpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.add_preferences_by_user(session.attributes["Current_User"], categoryslot, TVpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("RemovePreferenceIntent")
def remove_pref_intent(categoryslot, preferenceslot):
    """ removes a preference based on the preference name
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL 
        preferenceslot : an AMAZON.LITERAL """
    if categoryslot == "" or preferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], categoryslot, preferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("RemovePreferenceStockIntent")
def remove_pref_intent(categoryslot, stockpreferenceslot):
    """ removes a preference based on the preference name
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL 
        stockpreferenceslot : an AMAZON.LITERAL """
    if categoryslot == "" or stockpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], "stocks", stockpreferenceslot)
        msg = "Your preferences for {} are now {}".format("stocks", ud.get_preferences_by_user(session.attributes["Current_User"], "stocks"))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("RemovePreferenceBookIntent")
def remove_pref_intent(categoryslot, bookpreferenceslot):
    """ removes a preference based on the preference name
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL 
        bookpreferenceslot : an AMAZON.LITERAL """
    if categoryslot == "" or bookpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], categoryslot, bookpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("RemovePreferenceCharIntent")
def remove_pref_intent(categoryslot, charpreferenceslot):
    """ removes a preference based on the preference name
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL 
        charpreferenceslot : an AMAZON.LITERAL """
    if categoryslot == "" or charpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], categoryslot, charpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)

@ask.intent("RemovePreferenceTVIntent")
def remove_pref_intent(categoryslot, TVpreferenceslot):
    """ removes a preference based on the preference name
    
        Parameters
        ----------
        categoryslot : an AMAZON.LITERAL 
        TVpreferenceslot : an AMAZON.LITERAL """
    if categoryslot == "" or TVpreferenceslot == "":
        msg = "I could not understand. Please try again."
    elif session.attributes["Current_User"] is None:
        msg = "There is no current user saved."
    else:
        ud.remove_preferences_by_user(session.attributes["Current_User"], categoryslot, TVpreferenceslot)
        msg = "Your preferences for {} are now {}".format(categoryslot, ud.get_preferences_by_user(session.attributes["Current_User"], categoryslot))
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)


'''Switching profiles. (for now, based on img. Later will be based on voice)'''

def update_current_user():
    """ takes a pictre (future: voice sample) and matches it to a database
        returns either the current user or None if it cannot find it """
    if not "Current_User" in session.attributes:
        session.attributes["Current_User"] = None
    else:
        global temp_face_vectors
        '''can be called in the background of some functions!!!'''
        desc = f.get_one_face_descriptor_vector()
        temp_face_vectors = desc
        user = ud.compare_faces(desc)
        #record_to_file("temp",train=False) #create data
        #v_user = speaker_classifier_tflearn.test("temp.wav.ig") #call whenevr want to classify
        print("image: " + str(user))
        #print("voice: " + str(v_user))
        #if user is None:
        #    user = v_user
        session.attributes["Current_User"] = user

@ask.intent("CurrentUserIntent")
def check_user():
    """ checks what the current user is in front of it and assigns it to sessions.attributes["Current_User"]
        if user could not be found, assigns current_user to None
        is prompted if the user wants to add a profile
        if check is correct, updates face vectors based on profile """

    global checking_user
    update_current_user()
    if session.attributes["Current_User"] is None:
        msg = "I could not see anyone I identify. Would you like me to add a user?"
        checking_user = 1
    else:
        msg = "I see that {} is the current user. Is this correct?".format(session.attributes["Current_User"]) 
        checking_user = 2
    return question(msg)

@ask.intent("YesIntent")
def yes_intent():
    """ the Yes Intent. Does a whole lotta things. """
    
    global checking_user
    global adding_user
    global temp_name
    global temp_face_vectors
    if checking_user == 1:
        msg = "Please say the name of the user."
        checking_user = 3
        return question(msg)
    if checking_user == 2:
        msg = "Great. Thank you."
        checking_user = 0
        ud.update_face_vectors_by_user(session.attributes["Current_User"], temp_face_vectors)
        temp_face_vectors = 0
        return statement(msg)
    if checking_user == 4:
        msg = "The user has been added."
        checking_user = 0
        ud.update(temp_name, Profile(temp_name, f.get_one_face_descriptor_vector()))
        #record_to_file(temp_name)
        #speaker_classifier_tflearn.train()
        ud.save_obj("profiles_test_database.npy")
        session.attributes["Current_User"] = temp_name
        temp_name = ""
        return statement(msg)
    if adding_user == 2:
        msg = "The user has been added."
        adding_user = 0
        #ud.update(temp_name, Profile(temp_name, f.get_one_face_descriptor_vector()))
        #record_to_file(temp_name)
        speaker_classifier_tflearn.train()
        ud.save_obj("profiles_test_database.npy")
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
        del_user = False
        temp_name = ""
        ud.save_obj("profiles_test_database.npy")
        return statement(msg)
    else:
        msg = "I do not understand. Please try again."
        return statement(msg)

@ask.intent("NoIntent")
def no_intent():
    """ the No Intent. Does a whole lotta things. """
    global checking_user
    global adding_user
    global del_user
    global temp_face_vectors
    if checking_user == 1 and adding_user == 0:
        msg = "Alright. Thank you."
        session.attributes["Current_User"] = None
        checking_user = 0
        return statement(msg)
    if checking_user == 2 and adding_user == 0:
        msg = "My apologies. Please try again."
        checking_user = 0
        temp_face_vectors = 0
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
    """ the Name Intent. Does a whole lotta things. """
    
    global checking_user
    global adding_user
    global temp_name
    if nameslot == "" and checking_user == 3:
        msg = "I could not understand the name. Please repeat."
        return question(msg)
    elif checking_user == 3 and adding_user == 0:
        checking_user = 4
        temp_name = nameslot
        msg = "Is {} correct?".format(nameslot)
        return question(msg)
    elif adding_user == 1 and checking_user == 0:
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
    """ Adds a user based to the user database! """
    
    global adding_user
    global checking_user
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
    """ removes a user from the ud based on the name """
    
    global del_user
    global temp_name
    msg = "Are you sure you would like to delete {} from users?".format(remnameslot)
    temp_name = remnameslot
    del_user = True
    return question(msg)


'''Retake photo of current user!!/retake photo of specific user verbally'''

@ask.intent("RetakeCustomPicIntent")
def re_custom_pic_intent(recustompicslot):
    """ based on the name, retakes the picture for what's in front of it.
    
        Parameters
        ----------
        recustompicslot : an AMAZON.NAME  """
    
    if recustompicslot in ud.items():
        new_face_vectors = f.get_one_face_descriptor_vector()
        ud.get(recustompicslot).face_vectors = new_face_vectors
        msg = "The picture for user {} was successfully updated.".format(recustompicslot)
        ud.save_obj("profiles_test_database.npy")
    else:
        msg = "Could not find user in database. Please try again or add the user."
    return statement(msg)

@ask.intent("RetakePicIntent")
def re_pic_intent():
    """ based on the current user, retakes the picture for what's in front of it. """

    if session.attributes["Current_User"] is None:
        msg = "There is no current user. Please create a user or switch to another profile."
    else:
        new_face_vectors = f.get_one_face_descriptor_vector()
        ud.get(session.attributes["Current_User"]).face_vectors = new_face_vectors
        msg = "The picture for user {} was successfully updated.".format(session.attributes["Current_User"])
        ud.save_obj("profiles_test_database.npy")
    return statement(msg)


'''switch users verbally'''

@ask.intent("SwitchUserIntent")
def switch_user_intent(newuserlot):
    """ based on the name given, switches the current_user to the profile
    
        Parameters
        ----------
        newuserlot : an AMAZON.NAME  """
    
    if newuserlot in ud.names():
        session.attributes["Current_User"] = newuserlot
        msg = "Current user was successfully switched to {}".format(session.attributes["Current_User"])
    else:
        msg = "There is no user named {} in our database. Please try again or add this user.".format(newuserlot)
    return statement(msg)

'''add voice'''
#add intent later
#def add_voice_to_user(user_name):
#    record_to_file(user_name)
#    speaker_classifier_tflearn.train()

#add intent later
#@ask.intent("AddVoiceIntent")
#def add_voice_to_current_user():
#    record_to_file(session.attributes["Current_User"])
#    speaker_classifier_tflearn.train()
    
if __name__ == '__main__':
    app.run(debug=True)