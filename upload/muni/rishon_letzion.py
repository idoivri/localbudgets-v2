from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RishonLetzionMuni(AbstractMuni):

    fields = {0: CodeField,
              1: DescriptionField,
              4: AmountField}

    MUNI = 'rishon_letzion'
    info = {}



