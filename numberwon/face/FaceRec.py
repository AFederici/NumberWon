from camera import take_picture, use_camera
from dlib_models import download_model, download_predictor, load_dlib_models
download_model()
download_predictor()
from dlib_models import models
#import skimage.io as io
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cv2

load_dlib_models()
face_detect = models["face detect"]
face_rec_model = models["face rec"]
shape_predictor = models["shape predict"]


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
        fig, ax = plt.subplots()
        ax.imshow(pic)
        desc_list = []
        name_list = []
        detections = list(face_detect(pic, self.upscale))
        for i in range(len(detections)):
            l, r, t, b = detections[i].left(), detections[i].right(), detections[i].top(), detections[i].bottom()
            shape = shape_predictor(pic, detections[i])
            desc = np.array(face_rec_model.compute_face_descriptor(pic, shape))
            name = self.compare_faces(database, desc)
            desc_list.append(desc)
            name_list.append(name)
            ax.add_patch(Rectangle((l, b), r - l, t - b, Fill=None, alpha=1, color='yellow'))
            ax.text(l, b, name, color='white')
        return desc_list, name_list

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
        print(least)
        if least > 0.45:
            return "No match found"
        else:
            return least_key

    def update_faces(self, desc_list, name_list, database):
        """ updates the face-vector based on a new descriptor vector
            Parameters
            ----------
            desc_list : the descriptor vectors produced by the picture
            name_list : the list of names that match with the descriptor vectors
            database : the database """
        ans = input("Are the names and faces correctly matched? Unmatched faces will be added by your input. (y or n)")
        if ans == "y":
            for i in range(len(desc_list)):
                if name_list[i] == "No match found":
                    name = input("Please enter a name for this person.")
                    found = False
                    for x in database.items():
                        if name == x:
                            database.update_user_image(name, desc_list[i])
                            found = True
                    if found == False:
                        database.update(name, desc_list[i])
                else:
                    database.update_user_image(name_list[i], desc_list[i])
            print("database updated")
        else:
            print("database not updated")

    def file_read(self, file_id):
            
        """ reades a file on a computer
            Parameters
            ----------
            file_id : the filepath to read the file from """
        img_array = cv2.imread('file_id',1)

        if (img_array.shape[2] == 4):
            img_array = img_array[:, :, :3]
        return img_array

    def name_faces_from_picture(self, database):
        """ takes a picture and reads faces from that picture
            Parameters
            ----------
            database : the database """
        pic = self.take_picture()
        desc, names = self.find_faces(pic, database)
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")
        try:
            plt.pause(0.5)
        except Exception:
            pass
        self.update_faces(desc, names, database)

    def name_faces_from_file(self, file_id, database):
        """ takes a file and reads faces from that picture
            Parameters
            ----------
            file_id : the file to read from
            database : the database """
        pic = self.file_read(file_id)
        desc, names = self.find_faces(pic, database)
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")
        try:
            plt.pause(0.5)
        except Exception:
            pass
        self.update_faces(desc, names, database)

    def add_new_from_file(self, file_id, database):
        """ takes a file and ASSUMES that the face is a new one. Prompts the user to enter a new key for
            the face
            Parameters
            ----------
            file_id : the file to read from
            database : the database """
        pic = self.file_read(file_id)
        desc, names = self.find_faces(pic, database)
        desc = desc[0]
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")
        try:
            plt.pause(0.5)
        except Exception:
            pass
        name = input("Please enter a name for this person.")
        database.update(name, desc)

    def add_new_from_picture(self, database):
        """ takes a picture and ASSUMES that the face is a new one. Prompts the user to enter a new key for
            the face
            Parameters
            ----------
            database : the database """
        pic = self.take_picture()
        desc = self.find_faces(pic, database)
        desc = desc[0]
        warnings.filterwarnings("ignore", ".*GUI is implemented.*")
        try:
            plt.pause(0.5)
        except Exception:
            pass
        name = input("Please enter a name for this person.")
        database.update(name, desc)
