# TODO : create a db interface...

from pymongo import MongoClient
import csv

fields = ['code', 'name', 'amount']

MUNI = 'hura'

def handle_sheet(year,filename):
    client = MongoClient()
    db = client.database
    muni = db[MUNI]
    year_dataset = muni[year]
    reader = csv.DictReader(file(filename, 'rb'), fields)

    for line in reader:
        print "%s : %s" %(line['code'], line['amount'])
        if (line['name'] != '' and line['amount'].isdigit()):
            new_line  = {'name':line['name'], 'amount':line['amount'], 'code':line['code'] }
            year_dataset.insert(new_line);
    client.close() 
    
