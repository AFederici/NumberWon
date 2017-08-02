import numpy as np


class UserDatabase:
    def __init__(self, file=None):
        """ initializes an object of the Database class.
                Parameters
                ----------
                file : (default None) an old database object. (as .npy) If a file is specified, the data from that file is
                        transferred over """
        self.list_of_names = []
        if file is not None:
            self.dict = np.load(file).item()
            for i in self.dict:
                self.list_of_names.append(i)
        else:
            self.dict = {}

    def __repr__(self):
        """ The repr command """
        lines = []
        for names in self.dict.items():
            lines.append(str(names))
        return '\n'.join(lines)

    def items(self):
        """ returns the database's dictionary objects """
        return self.dict

    def names(self):
        return self.list_of_names

    def get(self, key):
        """ gets from the database's dictionary the obj based on the key """
        return self.dict[key]

    def save_obj(self, file_name='dictionary.npy'):
        """ saves the dictionary object
                Parameters
                ----------
                file_name : the name of the dictionary obj file that is being saved to be loaded at a later time """
        np.save(file_name, self.dict)
        return 'successfully saved'

    def switch_db(self, new_file, old_file_name='dictionary.npy'):
        """ switches databases based on a new file and an old file
                Parameters
                ----------
                new_file : the new database file name
                old_file_name : (default is the original database) the original file name """
        self.save_obj(old_file_name)
        self.__init__(new_file)
        return 'successfully loaded'

    def size(self):
        """ returns number of songs stored in the dictionary """
        return len(self.dict)

    def del_w_name(self, name):
        """ deletes a song from the database based on its id
                Parameters
                ----------
                _id :  the song id to be deleted """
        del self.dict[name]

    def get_user_by_name(self, name):
        """ search song by user
                Parameters
                ----------
                _id :  the song id to be deleted """
        if name in self.dict:
            return self.dict[name]
        else:
            return 'un-recognized user'

    def get_preferences_by_user(self, user, preference):
        """ returns a list of preferences """
        return self.dict[user].find_user_preferences(preference)

    def get_profile_status_by_user(self, user):
        """ returns the profile status of the specified user """
        return self.dict[user].profile_status

    def add_preferences_by_user(self, user, preference, preference_add):
        """ updates the preference list based on the user """
        self.dict[user].add_preference(preference, preference_add)

    def remove_preferences_by_user(self, user, preference, preference_rm):
        self.dict[user].del_preference(preference, preference_rm)

    def get_face_vector_by_user(self, user):
        return self.dict[user].face_vectors

    def update_face_vectors_by_user(self, name, new_face_vectors):
        """ takes the average of the olf descriptor vector and the new one to update """
        self.dict[name].update_face_vectors(new_face_vectors)

    def update(self, name, profile):
        """ adds a new val in the dictionary """
        self.dict[name] = profile
        self.list_of_names.append(name)

    def compare_faces(self, desc):
        """ Finds the best match face for a descriptor vector
            Parameters
            ----------
            database : the database
            desc : the descriptor vector produced by the picture; a (128,) shape descriptor

            Returns
            ----------
            least_key : the best-matched name for the descriptor vector """
        least = 1.0
        least_key = ""
        for key in self.items():
            v = np.sqrt(abs(np.sum((np.array(desc) - np.array(self.get_face_vector_by_user(key))) ** 2)))
            if least > v:
                least = v
                least_key = key
        print(least)
        print(least_key)
        if least > 0.59:
            return None
        else:
            return least_key
