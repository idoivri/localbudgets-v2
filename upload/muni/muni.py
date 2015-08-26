from server.models import Dataset
import csv
import logging

class Muni(object):
    """municipality class"""

    fields = []
    years = []
    muni = "Unknown"

    def __init__(self, print_data=False):
        self.print_data = print_data

    def handle_sheet( self, year, filename ):
        print "year: ",year
        # TODO: do this more generic than this!
        dataset = Dataset('raw', self.MUNI, year)
        reader = csv.reader(file(filename, 'rb'))

        if year in self.years:
            fields = self.years[year]
        else:
            fields = self.fields

        print "Fields:", fields


        for line in reader:
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
                invalid_fields = [' : '.join([field.name, field.value, field.error()]) 
                                  for field in line_fields if not field.is_valid()]
                #self.logger.info('invalid fields: %s', ' '.join(invalid_fields))
                print 'invalid fields: %s' %(' '.join(invalid_fields),)
        dataset.close()

    def print_str(self, data_str):
        if self.print_data:
            print data_str
