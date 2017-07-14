import numpy as np


class Database():
    def __init__(self, file = None):
        """ initializes an object of the Database class.
                Parameters
                ----------
                file : (default None) an old database object. (as .npy) If a file is specified, the data from that file is
                        transferred over

                Variables
                -------
                variation: Classification if the variation is a song or the footprint. variation describes what type of
                          dictionary it is, whether it is song id and titles or frequency and song id
                dict: a new dictionary to store songs.
                """
        self.variation = 'Not Specified'
        if file is not None:
            self.dict = np.load(file).item()
        else:
            self.dict = {}
        
    def def_variation(self, var):
        """ defines the variation, whether it be a song or a footprint.
                Parameters
                ----------
                var : (default None) a str named SONG or FP. (as .npy)"""
        self.variation = var
        
    def style(self):
        """ returns the variation style of the dictionary object """
        return 'Dict style is', self.variation
    
    def __repr__(self):
        """ The repr command; returns finger print followed by the song title and then artist """
        lines = ['Dictionary contains values of:', self.variation]
        for key, value in self.dict.items():
            lines.append('{}:{}'.format(key, value))
        return '\n'.join(lines)
        # delete this depending on what format the fp is in (possible hash), user might not care to see it
        
    def save_obj(self, file_name = 'dictionary.npy' ):
        """ saves the dictionary object
                Parameters
                ----------
                file_name : the name of the dictionary obj file that is being saved to be loaded at a later time """
        np.save(file_name, self.dict)
        return 'successfully saved'

    def switch_db(self, new_file, old_file_name = 'dictionary.npy'):
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

    def edit_values(self, key):
        """ edits a value in the database based on the dictionary key
                Parameters
                ----------
                key : the key of the obj that should be edited """
        new_val = input('What should the new value be?')
<<<<<<< HEAD
        self.dict[key] = new_val

=======
        self.dict[key] = (new_value)
        print (self.dict)
        #fix this to be more generalized
    
>>>>>>> 33c4c13249d5fd2b4e4a15c57b1650d667e0d7a8
    def add_song(self, _id, title = None, artist = None):
        """ checks if a song exists in the database and then adds it to the database.
                Parameters
                ----------
                _id :  the song id
                title : (default None) the title of the song
                artist : (default None) the artist of the song """
        if _id in self.dict:
            print('already in the dict')
        else:
            self.dict[_id] = (title, artist)
            
    def del_w_id(self, _id):
        """ deletes a song from the database based on its id
                Parameters
                ----------
                _id :  the song id to be deleted """
        del self.dict[_id]
            
    def del_w_title_and_artist(self, title, artist):
        """ deletes a song from the database based on its title and artist
                Parameters
                ----------
                title :  the song id to be deleted
                artist :  the song id to be deleted """
        del self.dict[self.get_id_by_song_and_artist(title, artist)]
        
    def get_song_by_id(self, _id):
        """ search song by id
                Parameters
                ----------
                _id :  the song id to be deleted """
        if _id in self.dict:
            return self.dict[_id]
        else:
            print('un-recognized song!')
        # still editing this method
        # can make it more user friendly by taking the input from the user and having the method call itself
        
    def get_id_by_song_and_artist(self, title, artist):
        """ search song id by title and artist
                Parameters
                ----------
                title :  the song id to be deleted
                artist :  the song id to be deleted """
        return list(self.dict.keys())[list(self.dict.values()).index((title, artist))]

    def add_freq_time(self, tuple_of_freq_time, tuple_of_id_time):
        """ update/add frequency and time for songs
                Parameters
                ----------
                tuple_of_freq_time :  tuple of frequencies for the song
                tuple_of_id_time :  tuple of times for the song """
        self.dict[tuple_of_freq_time] = tuple_of_id_time
    
    def del_w_freq(self, tuple_of_freq_time):
        """ delete song based on frequency
                Parameters
                ----------
                tuple_of_freq_time :  tuple of frequencies for the song """
        del self.dict[tuple_of_freq_time]
        
    def get_list_of_ids(self):
        """ returns a list of song ids produced from all of the tuples of frequencies and time """
        l = []
        for key in self.dict:
            l.append(self.dict[key][0])
        return l
