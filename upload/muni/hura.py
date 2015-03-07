# TODO : create a db interface...

from server.models import BudgetLine
from pymongo import MongoClient
import csv

fields = ['code', 'name', 'amount']

MUNI = 'hura'

def handle_sheet(year,filename):
    client = MongoClient()
    db = client.database
    muni = db[MUNI]
    reader = csv.DictReader(file(filename, 'rb'), fields)

    for line in reader:
        print "%s : %s" %(line['code'], line['amount'])
        if (line['name'] != '' and 
            line['amount'].isdigit()):
            new_line  = {'name':line['name'], 'amount':line['amount'], 'code':line['code'] }
            muni.insert(new_line);
        
    
