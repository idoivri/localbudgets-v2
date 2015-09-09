from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RehovotMuni(AbstractMuni):
     fields = {0: CodeField,
              1: DescriptionField,
              3: AmountField}

     MUNI = 'rehovot'
     info = {}
