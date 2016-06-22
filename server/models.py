### encoding: utf8 ###
from django.db import models
from pymongo import MongoClient
from settings import MONGO_SERVER
import itertools

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

DATABASE_NAME = 'munidatabase'
RAW_COLLECTION = 'raw'
MUNIS_COLLECTION = 'munis'
FLATTEN_COLLECTION = 'flatten'
SCHEME_COLLECTION = 'scheme'

def cleaner(func):
    def f(*args, **kwargs):
        ds = func(*args)
        if 'clean' in kwargs and kwargs['clean']:
            ds.drop()
        return ds
    return f


def _mongo_client():
    return MongoClient(MONGO_SERVER)
def _get_database(client):
    return client[DATABASE_NAME]

class Dataset():
    def __init__(self, pointer):
        self.client = _mongo_client()
        db = self.client[DATABASE_NAME]
        self.dataset = db
        # import pdb; pdb.set_trace()
        for arg in pointer:
            self.dataset = self.dataset[arg]
        # self.client = client
        # self.dataset = dataset

        # if clean:
        #    self.dataset.drop()

    def __getattr__(self, attr):
        return self.dataset.__getattribute__(attr)

    # def set_dataset(self,ds):
    #     self.dataset = ds

    def __enter__(self):
        return self

    def close(self):
        self.client.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

@cleaner
def get_raw_budget(muni,year):
    return Dataset([RAW_COLLECTION,muni,year])


# Depracated since it can't be closed. use get flatten
# @cleaner
# def get_budget(muni,year):
#     return Dataset([FLATTEN_COLLECTION]).find({'muni': muni,'year': year})

@cleaner
def get_flatten():
    return Dataset([FLATTEN_COLLECTION])

@cleaner
def get_munis():
    return Dataset([MUNIS_COLLECTION])

@cleaner
def get_scheme():
    return Dataset([SCHEME_COLLECTION])



@cleaner
def get_muni_years(muni_name):
    munis = get_munis()

    muni = munis.find_one({'name': muni_name})
    for year in sorted(muni['years']):
        yield year

    munis.close()

@cleaner
def get_muni_roots(muni_name):
    munis = get_munis()

    muni = munis.find_one({'name': muni_name})
    for year in sorted(muni['roots']):
        yield year
    munis.close()

@cleaner
def get_muni_info(muni_name):
    munis = get_munis()
    muni = munis.find_one({'name':muni_name})
    info = muni['info']
    munis.close()
    return dict(info)

def muni_iter(muni=None, years=None, **kws):
    if muni is None:
        with get_munis() as munis:
            muni_names = [muni['name'] for muni in munis.find()]

    for muni_name in muni_names:
        info = get_muni_info(muni_name)
        yield (muni_name,info)

            

def get_muni_names():
    for muni, info in muni_iter():
        yield (muni, info['heb_name'])

def del_database():
    client = _mongo_client()
    client.drop_database(DATABASE_NAME)


def del_collection(collection_name):
    client = _mongo_client()
    db = client[DATABASE_NAME]

    if collection_name in db.collection_names():
        collection = client[DATABASE_NAME][collection_name]
        collection.drop()

    client.close()
