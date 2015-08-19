from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class BeerMuni(AbstractMuni):
    fields = {0: CodeField,
              1: DescriptionField,
              3: AmountField}

    MUNI = 'beer_sheva'

