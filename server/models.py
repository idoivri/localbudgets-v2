### encoding: utf8 ###
from django.db import models
from pymongo import MongoClient
from settings import MONGO_SERVER

# TODO: put it somewhere else.
INFLATION = {1992: 2.338071159424868,
 1993: 2.1016785142253185,
 1994: 1.8362890269054741,
 1995: 1.698638328862775,
 1996: 1.5360153664058611,
 1997: 1.4356877762122495,
 1998: 1.3217305991625745,
 1999: 1.3042057718241757,
 2000: 1.3042057718241757,
 2001: 1.2860800081392196,
 2002: 1.2076314957018655,
 2003: 1.2308469660644752,
 2004: 1.2161648953888384,
 2005: 1.1878270593983091,
 2006: 1.1889814138002117,
 2007: 1.1499242230869946,
 2008: 1.1077747422214268,
 2009: 1.0660427753379829,
 2010: 1.0384046275616676,
 2011: 1.0163461588107117,
 2012: 1.0,
 2013: 1.0,
 2014: 1.0,
}

def _mongo_client():
    return MongoClient(MONGO_SERVER)

class Dataset():
    def __init__(self, collection, muni, year, clean=True):
        self.client = _mongo_client()
        db = self.client.database
        db = db[collection]
        munidb = db[muni]
        self.dataset = munidb[year]
    
    def __getattr__(self, attr):
        return self.dataset.__getattribute__(attr)
    
    def close(self):
        self.client.close()

def del_collection(self, collection):
    client = _mongo_client()
    collection = client.database[collection_name]
    collection.drop()
    client.close()
    
