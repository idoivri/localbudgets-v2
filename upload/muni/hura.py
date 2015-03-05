# TODO : create a db interface...

from server.models import BudgetLine
import csv

fields = ['code', 'name', 'amount']

MUNI = 'hura'

def handle_sheet(year,filename):
    # TODO: remove this. this is for debug perpesuse only.
    BudgetLine.objects.all().delete()
    reader = csv.DictReader(file(filename, 'rb'), fields)

    for line in reader:
        print "%s : %s" %(line['code'], line['amount'])
        if (line['name'] != '' and 
            line['amount'].isdigit()):
           BudgetLine(name = line['name'],
                      budget_id = line['code'],
                      amount = line['amount'],
                      year = year,
                      muni = MUNI).save()
        
    
