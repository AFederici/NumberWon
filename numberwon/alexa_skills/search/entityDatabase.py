from collections import Counter, defaultdict
import pickle
import string
import nltk
import re
from nltk.tokenize import word_tokenize
from search.searchEngine import MySearchEngine

class entityDatabase:
    def __init__(self):
        """
        Variables
        ------------------
            self.ent_dict: Dict[Str, list]
                key: link
                value: contains lists of string entities for each doc
            self.ent_dict2: Dict[Str, tuple]
                key: link
                value: lists of tuples(Str, int).
                the first element of each tuple is an entity, the second element is position in the raw text
            self.engine: MySearchEngine
                helps entityDatabase do doc_search, which is searching for most recent news about an entity
        """

        self.ent_dict = defaultdict(list)
        self.ent_dict2 = defaultdict(list)
        self.engine = MySearchEngine()

    def get_by_id(self, id):
        """ gets entities for a certain RSS Reuters link
        Parameters
        ----------
            id: string
             http link for a Reuters article

        Returns
        ----------
            list[str]
             returns a list of strings for link: id; strings are all the entities in that article"""

        return self.ent_dict[id]

    def entize(self, pickle, dictionary):
        #creates a dictionary where link = key, and value = list of entities
        """ Parameters
            ----------
                pickle: .pickle file
                 pickle stores a dictionary where keys = links and values = raw text of article for each link
                dictionary: Dict[str, list]
                 usually self.ent_dict, either as an empty or partially filled Dict

            Returns
            ----------
                dictionary: Dict[str, list]
                 returns a Dict where all the info from pickle is added to dictionary"""

        for key, val in pickle.items():
            tokens = nltk.word_tokenize(val)
            pos = nltk.pos_tag(tokens)
            named_entities = nltk.ne_chunk(pos, binary = True)
            for i in range(0, len(named_entities)):
                ents = named_entities.pop()
                if getattr(ents, 'label', None) != None and ents.label() == "NE":
                    z = list(zip(*[ne for ne in ents]))[0]
                    z = (" ".join(z)).lower()
                    dictionary[key].append(z)
        return dictionary

    def entize2(self, pickle, dictionary):
        # creates a dictionary where link = key, and value = list of tuples
        """ Parameters
            ----------
                pickle: .pickle file
                 pickle stores a dictionary where keys = links and values = raw text of article for each link
                dictionary: Dict[str, list]
                 usually self.ent_dict2, either as an empty or partially filled Dict

            Returns
            ----------
                dictionary: Dict[str, list]
                 returns a Dict where all the info from pickle is added to dictionary.
                 position of the entity in rawtext is stored as the second element of each tuple"""

        counter = 0
        for key, val in pickle.items():
            tokens = nltk.word_tokenize(val)
            pos = nltk.pos_tag(tokens)
            named_entities = nltk.ne_chunk(pos, binary = True)
            for i in range(0, len(named_entities)):
                ents = named_entities.pop()
                if getattr(ents, 'label', None) != None and ents.label() == "NE":
                    z = list(zip(*[ne for ne in ents]))[0]
                    z = ((" ".join(z)).lower(), counter)
                    dictionary[key].append(z)
                counter += len(ents)
        return dictionary

    def searchNentity(self, qword):
        # returns the top entity based on position in text
        """ Parameters
            ----------
                qword: str
                    string of terms that we complete a query on
            Returns
            ----------
                list[tuple]
                    list of tuples: (str, int)
                    first term is Entity, second term is how often the term appears next to qword
        """

        if self.engine.query(qword) != []:
            topdoc = self.engine.query(qword)[0][0]
            return self.top_entity_pos(qword,self.engine.raw_text[topdoc]) #Megan's method
        return None

    def docsearch(self, qword):
        #returns the top article most relevent to the query word, qword
        #what's new with qword?

        """
        Parameters
        ----------------
            qword: str
                search term
        Returns
        ----------------
            type: str
                first sentence of most relevant article
        """
        if self.engine.query(qword) != []:
            topdoc = self.engine.query(qword)[0][0]
            raw = self.engine.raw_text[topdoc] #whole doc
            return re.match(r'(?:[^.:;]+[.:;]){1}', raw).group().replace('\n\nFILE PHOTO', "") #first sentence
        return None

    def get_title_and_first_sentence(self, qword):
        #RETURN title And firSt SeNTENCE OF MOSt RELEVanT arTICLE
        #apologize for wACKY CASE
        return self.engine.whats_new(qword)

    def top_entity_pos(self, item, most_c=10):

        #search for item.
            #for i in feed. if i == feed:
        #create a list of words that are close to word in proximity
        #score based on proximity to word.
        #documents is already a list

        """
        #returns top entity based on distance from item when item occurs in texts
        :param item: str
            search term
        :param most_c: int
            optional parameter: number of entities to return
        :return: list[tuple]
            tuples contain most commonly found entities next to item in raw text
        """
        word_freq = Counter()
        for i in self.ent_dict2:
            #print(self.ent_dict2[i])
            for x in self.ent_dict2[i]:
                if x[0] == item:
                    for z in self.ent_dict2[i]:
                        if x[0] != z[0]:
                            #print((abs(x[1]-z[1])))
                            word_freq[z[0]] += 1/(abs((x[1]-z[1])))

        return word_freq.most_common(most_c)

    def top_entity_dict(self, item, most_c=10):
        #documents is already a list
        #turn each list into a counter, add all counters together.
        """
        #returns tuples contain most commonly associated with item across all docs

        :param item: str
            search term
        :param most_c: int
            optional parameter: number of entities to return
        :return: list[tuple]
            returned result is based on number of times it appears in articles item also appears in
        """
        mega_counter = Counter()
        for i in self.ent_dict:
            #get list of counters etc
            if item in self.ent_dict[i]:
                c = Counter(self.ent_dict[i])
                del c[item]
                mega_counter += c
        return mega_counter.most_common(most_c)

    def add_File_Database(self, pickle_path):
        #add a pickle file's contents to the database
        """
        #
        :param pickle_path: str
            system path to file
        """
        p = pickle.load(open(pickle_path, "rb"))
        self.engine.upload_vd(pickle_path)
        # pickle_path example: "C:\\Users\\User\\Desktop\\beaver\\NumberWon\\numberwon\\entity\\test.pickle"
        self.ent_dict = self.entize(p, self.ent_dict)
        self.ent_dict2 = self.entize2(p, self.ent_dict2)

    def add_Folder_Database(self, path_pickle_folder):
        #have paths in the form '/path/to/dir'
        #adds all pickle files in a
        """
        :param path_pickle_folder:
        """
        import os
        for f in os.listdir(path_pickle_folder):
            if f.endswith(".pickle"):
                p = pickle.load(open(path_pickle_folder + "/" + f, "rb"))
                self.engine.upload_vd(path_pickle_folder + "/" + f)
                self.ent_dict = self.entize(p, self.ent_dict)
                self.ent_dict2 = self.entize2(p, self.ent_dict2)
                #print(f, type(f))
