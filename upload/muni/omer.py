from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class OmerMuni(AbstractMuni):
    fields = {3: CodeField,
              4: DescriptionField,
              7: AmountField}  # TODO: make sure this is the right column number.

    MUNI = 'omer'

