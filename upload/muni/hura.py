from muni import Muni
from fields import AmountField, CodeField, DescriptionField

class HuraMuni(Muni):
    fields = {0: CodeField,
              1: DescriptionField,
              2: AmountField}

    MUNI = 'hura'

