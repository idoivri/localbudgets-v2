from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField


class KfarSabaMuni(AbstractMuni):
    MUNI = 'kfar_saba'

    fields = {0: CodeField,
              1: DescriptionField,
              8: AmountField}
    def __init__(self,**kwargs):
        super(KfarSabaMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(3)