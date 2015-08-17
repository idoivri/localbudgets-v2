from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class HuraMuni(AbstractMuni):
    fields = {0: CodeField,
              1: DescriptionField,
              2: AmountField}

    MUNI = 'hura'

