from camera import take_picture, use_camera
from dlib_models import download_model, download_predictor, load_dlib_models
download_model()
download_predictor()
from dlib_models import models
import skimage.io as io
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

load_dlib_models()
face_detect = models["face detect"]
face_rec_model = models["face rec"]
shape_predictor = models["shape predict"]

#idea: news buddy bases itself off of user preferences (users determined by face_rec)


class Face_Recognition:
    def __init__(self, upscale=1):
        """ initializes an object of the Database class.
            Parameters
            ----------
            upscale : (default 1) number of times to upscale image before detecting """
        self.upscale = upscale

    def take_picture(self):
        """ takes a picture and returns the img array """
        with use_camera() as camera:
            pic = take_picture()
        return pic
    
    def get_face_descriptor_vector(self):
        pic = self.take_picture()
        desc_list = []
        detections = list(face_detect(pic, self.upscale))
        for i in range(len(detections)):
            shape = shape_predictor(pic, detections[i])
            desc = np.array(face_rec_model.compute_face_descriptor(pic, shape))
            desc_list.append(desc)
        return desc_list
    
    def find_faces(self, pic, database):
        """ finds all of the faces in a picture and produces a picture with the faces highlighted
            Parameters
            ----------
            pic : the image array
            database : the database

            Returns
            ----------
            desc_list : the list of the descriptor vectors that describe the faces in the image
            name_list : the names matched to the faces """
        desc_list = []
        name_list = []
        detections = list(face_detect(pic, self.upscale))
        for i in range(len(detections)):
            shape = shape_predictor(pic, detections[i])
            desc = np.array(face_rec_model.compute_face_descriptor(pic, shape))
            name = self.compare_faces(database, desc)
            desc_list.append(desc)
            name_list.append(name)
        return desc_list, name_list, len(detections)

    def compare_faces(self, database, desc):
        """ Finds the best match face for a descriptor vector
            Parameters
            ----------
            database : the database
            desc : the descriptor vector produced by the picture; a (128,) shape descriptor

            Returns
            ----------
            least_key : the best-matched name for the descriptor vector """
        least = 1
        least_key = ""
        for key in database.items():
            v = np.sqrt(np.sum((desc - database.items()[key]) ** 2))
            if least > v:
                least = v
                least_key = key
        if least > 0.45:
            return "someone I do not know"
        else:
            return least_key

    def update_faces(self, desc_list, name_list, database):
        """ updates the face-vector based on a new descriptor vector
            Parameters
            ----------
            desc_list : the descriptor vectors produced by the picture
            name_list : the list of names that match with the descriptor vectors
            database : the database """
        for i in range(len(desc_list)):
            if not name_list[i] == "someone I do not know":
                database.update_user_image(name_list[i], desc_list[i])
        print("database updated")

    def name_faces_from_picture(self, database):
        """ takes a picture and reads faces from that picture
            Parameters
            ----------
            database : the database """
        pic = self.take_picture()
        desc, names, num_faces = self.find_faces(pic, database)
        names_c = ""
        for i in range(len(names)):
            if len(names) > 1 and len(names) != 2:
                if i == (len(names) - 1):
                    names_c += "and " + str(names[i])
                else:
                    names_c += str(names[i]) + ", "
            if len(names) == 2:
                if i == 0:
                    names_c += str(names[i]) + " and "
                else:
                    names_c += str(names[i])
            else:
                names_c =" ".join(names)
        return names_c , names, desc

    def add_face(self, database, name, desc):
        """ takes a picture and ASSUMES that the face is a new one. Prompts the user to enter a new key for
            the face
            Parameters
            ----------
            database : the database """
        #desc = desc[0]
        if not name in database.dict:
            database.update(name, desc)
        else:
            print("made a mistake")
            database.update_user_image(name, desc)
