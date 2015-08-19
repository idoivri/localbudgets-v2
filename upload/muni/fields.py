import re

class AbstractField(object):
    def __init__(self, line):
        self.value = line 
    def process(self):
        raise NotImplementedError("process is not implemented")

    def is_valid(self):
        return True

    def error(self):
        return ""
    

class AmountField(AbstractField):
    name = 'amount'
    def __init__(self, amount):
        #TODO: this is ugly, will be removed. Dash Yaniv.
        amount = amount.replace(',','')
        amount = amount[:amount.find('.')]
        self.value = amount.strip()

    def is_valid(self):
        return None != re.match("[-+]?[0-9]*", self.value)

    def process(self):
        if not self.is_valid:
            raise Exception("Amount Field is not valied")
        if self.value == '-' or self.value == '':
            return 0
        return int(self.value)


        
class CodeField(AbstractField):
    name = 'code'
    # TODO
    def process(self):

        print "ido:"+self.value

        return self.value
    
class DescriptionField(AbstractField):
    name = 'name'
    def process(self):
        return self.value

