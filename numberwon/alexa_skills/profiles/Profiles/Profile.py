#think of some machine learning ideas... generation??? identification???
class Profile:
    def __init__(self, name, face_vectors=None, pref_dict={}, profile_status=True):
        """ initializes an object of the Database class.
            Parameters
            ----------
            name : the name of the user
            face_vectors :
            pref_dict :
            profile_status :
            """
        self.name = name
        self.face_vectors = face_vectors
        self.pref_dict = pref_dict
        self.profile_status = profile_status

    def find_user_preferences(self, target_preference):
        if target_preference in self.pref_dict:
            return self.pref_dict[target_preference]
        else:
            return "Preference is not saved"

    def update_profile_status(self):
        self.profile_status = not self.profile_status

    def update_face_vectors(self, new_face_vectors):
        if self.face_vectors is None:
            self.face_vectors = new_face_vectors
        else:
            self.face_vectors = (self.face_vectors + new_face_vectors) /2

    def add_preference(self, pref_name, pref_list):
        if pref_name in self.pref_dict:
            self.pref_dict[pref_name].append(pref_list)
        else:
            self.pref_dict[pref_name] = pref_list

