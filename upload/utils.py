from pymongo import MongoClient

class Dataset():
   
    def __init__(self, muni, year):
        self.client = MongoClient()
        db = self.client.database
        munidb = db[muni]
        self.dataset = munidb[year]
    
    def __getattr__(self, attr):
        return self.dataset.__getattribute__(attr)
    
    def close(self):
        self.client.close()

