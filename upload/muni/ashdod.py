from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class AshdodAmount(AmountField):
    def __init__(self, amount):
        #TODO: this is ugly, will be removed. Dash Yaniv.
        amount = amount.replace(',','')
        amount = amount[:amount.find('.')]
        self.value = amount

class AshdodMuni(AbstractMuni):
    fields = ['code', 'name', 'amount']
    fields = {0: CodeField,
              1: DescriptionField,
              2: AshdodAmount}

    MUNI = 'ashdod'

