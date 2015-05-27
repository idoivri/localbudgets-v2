from pymongo import MongoClient

class Dataset():
    # TODO: use a abstract way to add this implemnetation and the upload implementation.
    def __init__(self, muni, year, clean=False):
        self.client = MongoClient()
        db = self.client.database
        if clean:
            db.drop_collection("tree.%s.%s" %(muni, year))
        db = db['tree']
        munidb = db[muni]
        self.dataset = munidb[year]

    def __getattr__(self, attr):
        return self.dataset.__getattribute__(attr)

    def close(self):
        self.client.close()





