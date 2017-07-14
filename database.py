import numpy as np
class Database():
    def __init__(self, file = None):
        self.variation = 'Not Specified' #ideally song or fp if the user uses correctly
        #variation describes what type of dictionary it is, whether it is song id and titles or frequency and song id
        #check to see if the user wants to load in a file (as a .npy)
        if file is not None:
            self.dict = np.load(file).item()
        else:
            self.dict = {}
        #creates new dictionary unless on is loaded in
        
    def def_variation(self, var):
        #have the var be either named SONG or FP
        self.variation = var
        
    def style(self):
        return 'Dict style is', self.variation
    
    def __repr__(self):
        lines = ['Dictionary contains values of:', self.variation]
        for key, value in self.dict.items():
            lines.append('{}:{}'.format(key, value))
        return '\n'.join(lines)
            #delete this depending on what format the fp is in (possible hash), user might not care to see it
            #returns finger print followed by the song title and then artist
        
    def save_obj(self, file_name = 'dictionary.npy' ):
        np.save(file_name, self.dict)
        return 'successfully saved'
        #saves the dictionary as a file to load at a later time

    def switch_db(self, new_file, old_file_name = 'dictionary.npy'):
        self.save_obj(old_file_name)
        self.__init__(new_file)
        return 'successfully loaded'
        #make sure new_file is a strng ending in npy
        #will re-initializing corrupt old file data even though its already been saved?
        
    def size(self):
        return len(self.dict)
        #returns number of songs stored in the dictionary
        
    def edit_values(self, key):
        new_val = input('What should the new value be?')
        self.dict[key] = (new_value)
        print (self.dict)
        #fix this to be more generalized
    
    def add_song(self, _id, title = None, artist = None):
        #check if it already exists
        #not sure if author, title tuple would be better as key or as value, depends on fp alg
        #requires title and fp, author optional, maybe find a way to make it either or for song and author
        if _id in self.dict:
            print('already in the dict')
        else:
            self.dict[_id] = (title , artist)
            
    def del_w_id(self, _id):
        del self.dict[_id]
            
    def del_w_title_and_artist(self, title, artist):
        del self.dict[self.get_id_by_song_and_artist(title, artist)]
        
    def get_song_by_id(self, _id):
        #search song by fingerprint
        if _id in self.dict:
            return self.dict[_id]
        else:
            print('un-recognized song!')
        #still editing this method
        #can make it more user friendly by taking the input from the user and having the method call itself
        
    def get_id_by_song_and_artist(self, title, artist):
        return(list(self.dict.keys())[list(self.dict.values()).index((title, artist))])
        #finds the fingerprint by searching with artist and title, inconvenient but shouldnt be that necessary anyways
        
    ###BELOW HERE ARE METHODS FOR KEY OF FREQUENCIES AND T AND VALUES OF SONG ID AND TIME
    def add_freq_time(self, tuple_of_freq_time, tuple_of_id_time):
        self.dict[tuple_of_freq_time] = tuple_of_id_time
    
    def del_w_freq(self, tuple_of_freq_time):
        del self.dict[tuple_of_freq_time]
        
    def get_list_of_ids(self):
        l = []
        for key in self.dict:
            l.append(self.dict[key][0])
        return l
    #returns a list of song ids produced from all of the tuples of frequencies and time
