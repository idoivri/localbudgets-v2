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


class Attr(object):
    # default_value = None
    # years_value = {}
    def __init__(self, default_value=None):
        self.default_value = default_value
        self.years_value = {}
    def add_value(self,value,year=None):
        if year is not None:
            self.years_value[year]=value
        else:
            self.default_value = value


    def __call__(self,year, *args, **kwargs):
        if year in self.years_value:
            return self.years_value[year]
        else:
            return self.default_value


class AbstractMuni(object):
    """municipality class"""
    __metaclass__ = MetaMuni

    MUNI = "Unknown"

    start_in_row = Attr(0)
    data_fields = Attr()


    def __init__(self, print_data=False, clean=False):
        self.print_data = print_data
        self.clean = clean
        self.default_values = {'start_in_row': 0,
                      'data_fields': []}
        if hasattr(self, 'fields'):
            self.data_fields.add_value(self.fields)
        if hasattr(self, 'years'):
            for year in self.years:
                self.data_fields.add_value(self.years[year],year)


    def handle_sheet(self, year, filename):
        print 'handling file: %s' %(filename,)

        dataset = get_raw_budget(self.MUNI, year, clean = self.clean)
        if dataset.count()>0 and not self.clean:
            print "Budget for %s, in year %d already exists. Use --clean to overwrite."%(self.MUNI,year)
            return

        reader = csv.reader(file(filename, 'rb'))

        fields = self.data_fields(year)

        start_in_row = self.start_in_row(year)

        for line_number, line in enumerate(reader):
            if line_number>=start_in_row:
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
