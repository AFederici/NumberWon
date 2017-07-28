from flask import Flask
from flask_ask import Ask, statement, question
import requests
import time
import unidecode
import json
from FaceRec import Face_Recognition
from database import Database
import numpy as np
f = Face_Recognition()
d = Database("goodfile.npy")
num_faces = 0
name = ""
feature_vector = np.array([])
global face_detect
face_detect = False
global start
start = False
global asking_about_names
asking_about_names = False
global asking_about_database
asking_about_database = False
global asked_about_database
asked_about_database = False

app = Flask(__name__)
ask = Ask(app, '/')



#fix so that Echo can ask if ans is right, and then update it based off of what user inputs.

@app.route('/')
def homepage():
    return "Face Rec"

@ask.launch
def start_skill():
    global face_detect
    face_detect = False
    global asking_about_names
    asking_about_names = False
    global asking_about_database
    asking_about_database = False
    global asked_about_database
    asked_about_database = False
    msg = "Hello. May I see your face?"
    global start
    start = True
    return question(msg)

def take_picture():
    names = f.name_faces_from_picture(d)
    print(names)
    return names

@ask.intent("YesIntent")
def name_faces():
    num_faces = 0
    global face_detect
    if not face_detect:
        names, names_list, desc_vectors = take_picture()
        global num_faces
        num_faces = len(desc_vectors)
        global feature_vector
        feature_vector = desc_vectors
        faces_msg = "I see {}. Is that correct?".format(names)
        global face_detect
        face_detect = True
        global asking_about_database
        asking_about_database = True
        global start
        start = False
        return question(faces_msg)
    global asking_about_names
    if asking_about_names:
        msg = "Adding {} to the database.".format(name)
        f.add_face(d, name, feature_vector)
        #d.save_obj("goodfile.npy")
        global asking_about_names
        asking_about_names = False
        return statement(msg)
    global asking_about_database
    if asking_about_database:
        msg = "Would you like me to update the database?"
        asking_about_database = False
        global asked_about_database
        asked_about_database = True
        return question(msg)
    else:
        state = "Great. Optimizing database based on correct results."
        global feature_vector
        global names_list
        global d
        f.update_faces(feature_vector, names_list, d)
        #d.save_obj("goodfile.npy")
        return statement(state)
    
@ask.intent("NoIntent")
def no_intent():
    global start
    if start:
        print(start)
        msg = "Ok, thanks. Have a nice day."
        return statement(msg)
    global asking_about_names
    if asking_about_names:
        msg = "My apologies. Please say the correct name again."
        return question(msg)
    global asked_about_database
    if asked_about_database:
        msg = "Ok, thanks. Have a nice day."
        asked_about_database = False
        return statement(msg)
    else:
        global num_faces
        if num_faces > 1:
            msg = "My apologies. Please re-take the picture with only the unidentified person."
            return statement(msg)
        else:
            msg = "Please say the correct name."
            asking_about_names = True
            return question(msg)

@ask.intent("Melanie")
def name_intent(nameslot):
    print("name: " + str(nameslot))
    global name
    name = nameslot
    msg = "Is {} correct?".format(nameslot)
    return question(msg)
    
if __name__ == '__main__':
    app.run(debug=True)