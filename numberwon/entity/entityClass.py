class entityDatabase:

    from collections import Counter, defaultdict
    import nltk, pickle
    from nltk.tokenize import word_tokenize
    import MySearchEngine as engine

    def __init__(self, pickle_path):
        self.ent_dict = defaultdict(list)
        p = pickle.load(open(pickle_path), "rb")
        #pickle_path example: "C:\\Users\\User\\Desktop\\beaver\\NumberWon\\numberwon\\entity\\test.pickle"
        self.entize(p)
    def get_by_id(self, id):
        return self.ent_dict[id]
    def entize(self, pickle):
        for key, val in pickle.items():
            tokens = nltk.word_tokenize(val)
            pos = nltk.pos_tag(tokens)
            named_entities = nltk.ne_chunk(pos, binary = True)
            for i in range(0, len(named_entities)):
                ents = named_entities.pop()
                if getattr(ents, 'label', None) != None and ents.label() == "NE":
                    z = list(zip(*[ne for ne in ents]))[0]
                    z = (" ".join(z),)
                    self.ent_dict[key].append(z)
    def searchNentity(qword):
        topdoc = engine.query(qword)[0][0]
        return top_entity_associated_with_item(qword,engine.raw_text[topdoc]) #Megan's method

    def docsearch(qword):
        topdoc = engine.query(qword)[0][0]
        raw = engine.raw_text[topdoc] #whole doc
        return re.match(r'(?:[^.:;]+[.:;]){1}', raw).group() #first sentence
    def top_entity_associated_with_item(item, documents, weighted=True, rangee=5):
        #search for item.
            #for i in feed. if i == feed:
        #create a list of words that are close to word in proximity
        #score based on proximity to word.
        word_freq = Counter()
        for i in documents:
            old_spli = word_tokenize(i)
            spli = []
            for i in old_spli:
                if i not in string.punctuation:
                    spli.append(i.lower())
            for x in range(len(spli)):
                if spli[x] == item:
                    for z in range(rangee):
                        if not (x - z < 0):
                            if spli[x-z] != spli[x]:
                                if weighted:
                                    word_freq[spli[x-z]] += 1/abs((x -(x-z)))
                                else:
                                    word_freq[spli[x-z]] += 1
                        if not (x + z > (len(spli) - 1)):
                            if spli[x+z] != spli[x]:
                                if weighted:
                                    word_freq[spli[x+z]] += 1/abs((x -(x+z)))
                                else:
                                    word_freq[spli[x+z]] += 1
        return word_freq.most_common()