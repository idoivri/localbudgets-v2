#TODO : create a db interface...
from upload.utils import Dataset
import csv

fields = ['code', 'name','temp', 'amount']

MUNI = 'beer-sheva'

def handle_sheet(year, filename):
    dataset = Dataset(MUNI, year)
    reader = csv.DictReader(file(filename, 'rb'), fields)

    for line in reader:
        print "%s : %s" %(line['code'], line['amount'])
        if (line['name'] != '' and line['amount'].isdigit()):
            new_line  = {'name':line['name'], 'amount':line['amount'], 'code':line['code'] }
            print(new_line);
            dataset.insert(new_line);
    dataset.close()