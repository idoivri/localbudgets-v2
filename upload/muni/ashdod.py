from upload.utils import Dataset
from abstract_muni import AbstractMuni
import csv

class Muni(AbstractMuni):
    fields = ['code', 'name', 'amount']

    MUNI = 'ashdod'

    def handle_sheet(self, year, filename):
        dataset = Dataset(self.MUNI, year)
        reader = csv.DictReader(file(filename, 'rb'), self.fields)

        for line in reader:
            self.print_str("%s : %s" %(line['code'], line['amount']))
            new_line  = {'name':line['name'], 'amount':line['amount'], 'code':line['code'] }
            self.print_str(new_line)
            dataset.insert(new_line)
        dataset.close()