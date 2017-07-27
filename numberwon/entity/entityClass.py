class entityDatabase:
    from collections import Counter, defaultdict
    def __init__(self):
        self.ent_dict = dict()
    def addbyDoc(self, doc_id, entity):
        ent_dict[doc_id] = entity