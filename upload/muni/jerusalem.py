from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField



class JerusalemMuni(AbstractMuni):
    fields = {2: CodeField,
              1: DescriptionField,
              0: AmountField}

    MUNI = 'jerusalem'
    def __init__(self,**kwargs):
        self.start_in_row.add_value(3)
        super(JerusalemMuni, self).__init__(**kwargs)