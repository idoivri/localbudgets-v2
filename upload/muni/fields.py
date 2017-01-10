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
        self.value = amount
        amount = amount.replace(',','')
        amount = amount.split('.')[0]
        self.amount = amount.strip()

    def is_valid(self):
        return None != re.match("^[-+]?[0-9]*$", self.amount)

    def process(self):
        if not self.is_valid():
            raise Exception("Amount Field is not valied (%s)" %(self.value, ))
        if self.amount == '-' or self.amount == '':
            return 0

        return abs(int(self.amount))


        
class CodeField(AbstractField):
    name = 'code'
    def process(self):
        return self.value.replace("-", '').replace(' ','')
    def is_valid(self):
        return '' != self.process()
    
class DescriptionField(AbstractField):
    name = 'name'
    def process(self):
        return self.value

