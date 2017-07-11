from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RamatGanMuni(AbstractMuni):
    MUNI = 'ramat_gan'
    def __init__(self,**kwargs):
        super(RamatGanMuni, self).__init__(**kwargs)
        self.data_fields.add_value({1: CodeField,
              5: DescriptionField,
              6: AmountField})
        self.start_in_row.add_value(1)
