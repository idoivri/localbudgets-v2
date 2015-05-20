#TODO : create a db interface...
from server.models import Dataset
from abstract_muni import AbstractMuni
import csv

class Muni(AbstractMuni):
    fields = ['code', 'name', 'amount']
    MUNI = 'qiryat_bialik'

    def handle_sheet(self, year, filename):
        dataset = Dataset('raw', self.MUNI, year)
        reader = csv.DictReader(file(filename, 'rb'), self.fields)

        for line in reader:
            self.print_str("%s : %s" %(line['code'], line['amount']))
            if (line['name'] != '' and line['amount'].isdigit()):
                new_line  = {'name':line['name'], 'amount':line['amount'], 'code':line['code'] }
                dataset.insert(new_line);
        dataset.close()
