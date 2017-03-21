from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class AshdodMuni(AbstractMuni):
    fields = {0: CodeField,
              1: DescriptionField,
              2: AmountField}
    fields_2016 = {1: CodeField,
              2: DescriptionField,
              7: AmountField}
    MUNI = 'ashdod'
    years = {2016: fields_2016}
    def __init__(self,**kwargs):
        self.start_in_row.add_value(0)
        self.start_in_row.add_value(1,year=2016)
        super(AshdodMuni,self).__init__(**kwargs)