from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField



class AshdodMuni(AbstractMuni):
    fields = ['code', 'name', 'amount']
    fields = {0: CodeField,
              1: DescriptionField,
              2: AmountField}

    MUNI = 'ashdod'

