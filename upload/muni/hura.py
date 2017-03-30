from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class HuraMuni(AbstractMuni):
    fields = {0: CodeField,
              1: DescriptionField,
              7: AmountField}  # TODO: make sure this is the right column number.

    MUNI = 'hura'

    def __init__(self,**kwargs):
        super(HuraMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(3)
