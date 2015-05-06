class AbstractMuni(object):
    """abstract municipality class"""
	
    def __init__(self, fields, print_data=False):
        self.print_data = print_data
        self.fields = fields
	
    def handle_sheet( self ):
        dataset = Dataset('raw', self.MUNI, year)
        reader = csv.DictReader(file(filename, 'rb'), self.fields) #TODO: make regular reader

        for line in reader:
            new_line = {}
			valid_line = True
            for index in self.fields.keys()
                field = self.fields[index]
                if field.is_valid(line[index]):
                    new_line[field.name] = field.process(line[index])
				else:
                    valid_line = False
                    break					
            if valid_line:
                self.print_str("%s : %s" %(line['code'], line['amount']))
                self.print_str(new_line)
                dataset.insert(new_line)
        dataset.close()

    def print_str(self, str):
	    if self.print_data:
		    print str