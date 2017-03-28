from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RamatGanMuni(AbstractMuni):
    MUNI = 'ramat_gan'
    def __init__(self,**kwargs):
        self.data_fields.add_value({0: CodeField,
              5: DescriptionField,
              6: AmountField})
        self.start_in_row.add_value(1)
        super(RamatGanMuni, self).__init__(**kwargs)