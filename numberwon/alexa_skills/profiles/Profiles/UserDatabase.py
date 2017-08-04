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
        """ returns the list of user names """
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
                name : name of the user """
        del self.dict[name]

    def get_user_by_name(self, name):
        """ search song by user
                Parameters
                ----------
                name :  the name of the user to find

                Returns
                ---------
                either self.dict[name] or None if the user cannot be recognized """

        if name in self.dict:
            return self.dict[name]
        else:
            return None

    def get_preferences_by_user(self, user, category):
        """ gets preferences based off of category
                Parameters
                ----------
                user :  the name of the user to find preferences for
                preference :  the name of the category to find preferences

                Returns
                ---------
                a list of preferences (str) """

        return self.dict[user].find_user_preferences(category)

    def add_preferences_by_user(self, user, category, preference_add):
        """ adds a preference to a list of (category) preferences
                Parameters
                ----------
                user :  the name of the user to find preferences for
                category :  the name of the category to find preferences
                preference_add : the preference to add

                Returns
                ---------
                nothing """

        self.dict[user].add_preference(category, preference_add)

    def remove_preferences_by_user(self, user, category, preference_rm):
        """ removes a preference from a list of (category) preferences
                Parameters
                ----------
                user :  the name of the user to find preferences for
                category :  the name of the category to find preferences
                preference_rm : the preference to remove

                Returns
                ---------
                nothing """

        self.dict[user].del_preference(category, preference_rm)

    def get_face_vector_by_user(self, user):
        """ gets the face vector of the user
                Parameters
                ----------
                user :  the name of the user to get face vectors for

                Returns
                ---------
                a np array of the face vector """

        return self.dict[user].face_vectors

    def update_face_vectors_by_user(self, user, new_face_vectors):
        """ takes the average of the old descriptor vector and the new one to update
                Parameters
                ----------
                user :  the name of the user to update face vector
                new_face_vectors :  the new np array of face vectors

                Returns
                ---------
                nothing """

        self.dict[user].update_face_vectors(new_face_vectors)

    def update(self, user, profile):
        """ adds a new user in the dictionary and adds their name to the list of names
                Parameters
                ----------
                user :  the name of the user to update face vector
                profile :  the Profile object to add

                Returns
                ---------
                nothing """

        user = user.lower()
        self.dict[user] = profile
        self.list_of_names.append(user)

    def compare_faces(self, desc):
        """ Finds the best match face for a descriptor vector
            Parameters
            ----------
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
