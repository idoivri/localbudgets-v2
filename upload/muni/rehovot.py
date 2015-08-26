from muni import Muni
from fields import AmountField, CodeField, DescriptionField

class RehovotMuni(Muni):
     fields = {0: CodeField,
              1: DescriptionField,
              3: AmountField}

     MUNI = 'rehovot'