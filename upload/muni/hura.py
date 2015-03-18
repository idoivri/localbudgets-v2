#TODO : create a db interface...
from upload.utils import Dataset
import csv

fields = ['code', 'name', 'amount']

MUNI = 'hura'

def handle_sheet(year, filename):
    dataset = Dataset(MUNI, year)
    reader = csv.DictReader(file(filename, 'rb'), fields)

    for line in reader:
        print "%s : %s" %(line['code'], line['amount'])
        if (line['name'] != '' and line['amount'].isdigit()):
            new_line  = {'n    ame':line['name'], 'amount':line['amount'], 'code':line['code'] }
            dataset.insert(new_line);
    dataset.close()