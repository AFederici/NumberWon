class Profile:
    def __init__(self, name, face_vectors=None, pref_dict={}, profile_status=False):
        """ initializes an object of the Profile class.
                Parameters
                ----------
                name :  the name of the user
                face_vectors : a np array of face vectors
                pref_dict : a dictionary {"key" : [] )} of preferences
                profile_status : not needed, please ignore. Default is False """

        self.name = name.lower()
        self.face_vectors = face_vectors
        self.pref_dict = pref_dict
        self.profile_status = profile_status

    def get_name(self):
        """ returns the name of the user """

        return self.name

    def find_user_preferences(self, category):
        """ finds the preferences of the user
                Parameters
                ----------
                category :  the category of preference to find

                Returns
                ---------
                the list of preferences or None if category is not in dict """

        if category in self.pref_dict:
            return self.pref_dict[category]
        else:
            return None

    def update_face_vectors(self, new_face_vectors):
        """ takes the average of the face vectors and makes it a new face vector
                Parameters
                ----------
                new_face_vectors :  a new np array of face vectors

                Returns
                ---------
                nothing """

        if self.face_vectors is None:
            self.face_vectors = new_face_vectors
        else:
            self.face_vectors = (self.face_vectors + new_face_vectors) /2

    def add_preference(self, category, pref_list):
        """ adds a preference to a list based on the key (category)
                Parameters
                ----------
                category :  the category of preference (news, fanfiction, etc...)
                pref_list : the list of preferences to add

                Returns
                ---------
                nothing """

        if category in self.pref_dict:
            self.pref_dict[category] += [pref_list]
        else:
            self.pref_dict[category] = [pref_list]

    def del_preference(self, category, pref_to_rm):
        """ removes a preference to a list based on the key (category)
                Parameters
                ----------
                category :  the category of preference (news, fanfiction, etc...)
                pref_to_rm : the specific preference to remove

                Returns
                ---------
                nothing """

        if category in self.pref_dict:
            new_l = []
            for i in self.pref_dict[category]:
                if not i == pref_to_rm:
                    new_l.append(i)
            self.pref_dict[category] = new_l

