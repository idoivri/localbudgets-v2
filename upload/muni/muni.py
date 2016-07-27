from server.models import get_raw_budget
import csv
import logging
from muni_info import infos

class MetaMuni(type):
    # TODO: fix me we might not need a metaclass for this problem...
    def __new__(cls, name, bases, dct):
        if name is not 'AbstractMuni':
            if dct['MUNI'] not in infos:
                raise Exception("There is no information about muni: %s in the file muni_info.py" 
                                %(dct['MUNI'],))
            dct['info'] = infos[dct['MUNI']]
            
        return super(MetaMuni, cls).__new__(cls, name, bases, dct)

class AbstractMuni(object):
    """municipality class"""
    __metaclass__ = MetaMuni

    fields = []
    years = []
    MUNI = "Unknown"

    def __init__(self, print_data=False, clean=False):
        self.print_data = print_data
        self.clean = clean

    def handle_sheet(self, year, filename):
        print 'handling file: %s' %(filename,)

        dataset = get_raw_budget(self.MUNI, year, clean = self.clean)
        if dataset.count()>0 and not self.clean:
            print "Budget for %s, in year %d already exists. Use --clean to overwrite."%(self.MUNI,year)
            return

        reader = csv.reader(file(filename, 'rb'))

        if year in self.years:
            fields = self.years[year]
        else:
            fields = self.fields

        for line_number, line in enumerate(reader):
            new_line = {}

            line_fields = [fields[index](line[index])
                                for index in fields]

            # check validity of line and write valid lines to DB
            fields_are_valid = [field.is_valid() for field in line_fields]

            if all(fields_are_valid):
                for field in line_fields:
                    # process fields
                    new_line[field.name] = field.process()

                # insert line data to DB
                self.print_str(new_line)

                dataset.insert(new_line)
            else:
                invalid_fields = [':'.join([field.name, field.value, field.error()]) 
                                  for field in line_fields if not field.is_valid()]
                #self.logger.info('invalid fields: %s', ' '.join(invalid_fields))
                print 'invalid fields in line %d : %s' %(line_number+1, ', '.join(invalid_fields),)
        dataset.close()

    def print_str(self, data_str):
        if self.print_data:
            print data_str
