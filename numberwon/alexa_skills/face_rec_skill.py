from flask import Flask
from flask_ask import Ask, statement, question
from face.FaceRec import Face_Recognition
from face.database import Database
import numpy as np

f = Face_Recognition()
d = Database("goodfile.npy")
num_faces = 0
name = ""
feature_vector = np.array([])
global state
state = 0

app = Flask(__name__)
ask = Ask(app, '/')


@app.route('/')
def homepage():
    return "Face Rec"


@ask.launch
def start_skill():
    """starts by asking a question"""
    msg = "May I see your face?"
    return question(msg)


def take_picture():
    """takes the user's picture"""
    names = f.name_faces_from_picture(d)
    return names


@ask.intent("YesIntent")
def name_faces():
    """runs if the user says yes"""
    global state
    if state == 0:
        global names_list
        names, names_list, desc_vectors = take_picture()
        global num_faces
        num_faces = len(desc_vectors)
        global feature_vector
        feature_vector = desc_vectors
        if len(names_list) == 1 and names == "someone I do not know":
            faces_msg = "I see someone I do not know. Would you like me to add this person to the database?"
            global state
            state = 4
            return question(faces_msg)
        else:
            faces_msg = "I see {}. Is that correct?".format(names)
            state += 1
            return question(faces_msg)
    elif state == 1:
        msg = "Would you like me to update the database?"
        state += 1
        return question(msg)
    elif state == 2:
        msg = "Great. Optimizing database based on correct results."
        global feature_vector
        global names_list
        global d
        f.update_faces(feature_vector, names_list, d)
        d.save_obj("goodfile.npy")
        global state
        state = 0
        return statement(msg)
    elif state == 3:
        msg = "Adding {} to the database.".format(name)
        f.add_face(d, name, feature_vector)
        d.save_obj("newfile.npy")
        global state
        state = 0
        return statement(msg)
    elif state == 4:
        msg = "Please say the correct name."
        global state
        state = 5
        return question(msg)
    elif state == 5:
        msg = "Adding {} to the database.".format(name)
        f.add_face(d, name, feature_vector)
        d.save_obj("goodfile.npy")
        global state
        state = 0
        return statement(msg)
    else:
        msg = "Something went wrong. Please try again."
        return statement(msg)

@ask.intent("NoIntent")
def no_intent():
    """runs if the user says no"""
    global state
    if state == 0:
        msg = "Ok, thanks. Have a nice day."
        global state
        state = 0
        return statement(msg)
    elif state == 1:
        global num_faces
        if num_faces > 1:
            msg = "My apologies. Please re-take the picture with only the unidentified person."
            global state
            state = 0
            return statement(msg)
        else:
            msg = "Please say the correct name."
            global state
            state = 3
            return question(msg)
    elif state == 2:
        msg = "Ok, thanks. Have a nice day."
        global state
        state = 0
        return statement(msg)
    elif state == 3:
        msg = "My apologies. Please say the correct name again."
        return question(msg)
    elif state == 4:
        msg = "Ok, thanks. Have a nice day."
        global state
        state = 0
        return statement(msg)
    elif state == 5:
        msg = "My apologies. Please say the correct name again."
        return question(msg)
    else:
        msg = "Something went wrong. Please try again."
        return statement(msg)

@ask.intent("NameIntent")
def name_intent(nameslot):
    """gets the name that the user says"""
    print("name: " + str(nameslot))
    global name
    name = nameslot
    msg = "Is {} correct?".format(nameslot)
    return question(msg)


if __name__ == '__main__':
    app.run(debug=True)
