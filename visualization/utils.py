from pymongo import MongoClient

class Dataset():
    # TODO: use a abstract way to add this implemnetation and the upload implementation.
    def __init__(self, muni, year, clean=False):
        self.client = MongoClient()
        db = self.client.database
        db = db['tree']
        if clean:
            db.drop_collection("%s.%s" %(muni, year))
        munidb = db[muni]
        self.dataset = munidb[year]

    def __getattr__(self, attr):
        return self.dataset.__getattribute__(attr)

    def close(self):
        self.client.close()





class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', 
                       code=None, 
                       amount=None, 
                       children=None):
        self.name = name
        self.amount = amount
        self.code = code
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        # return str(self.code)
        return (str(self.code) + 
                "(" + 
                ", ".join(map(repr,self.children)) + 
                ")")

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def to_dict(self):
        return {'code': self.code,
                'amount': self.amount,
                'name': self.name,
                'children': [i.to_dict() for i in self.children]}

    @classmethod
    def from_dict(cls,dictionary):
        print repr(dictionary)
        dictionary['children'] = [cls.from_dict(child) 
                                  for child in dictionary['children']]

        # FIXME: might be problomatic but it's prety :)
        root = cls(**dictionary)

        return root
