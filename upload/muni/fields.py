import re

class AbstractField(object):
    def __init__(self, line):
        self.value = line 
    def process(self):
        raise NotImplementedError("process is not implemented")

    def is_valid(self):
        return True

    def error(self):
        return "Unknow"

class AmountField(AbstractField):
    name = 'amount'

    def is_valid(self):
        return None != re.match("[-+]?[0-9]+", self.value)

    def process(self):
        if not self.is_valid:
            raise Exception("Amount Field is not valied")
        return int(self.value)


        
class CodeField(AbstractField):
    name = 'code'
    # TODO
    def process(self):
        return self.value
    
class DescriptionField(AbstractField):
    name = 'name'
    def process(self):
        return self.value

