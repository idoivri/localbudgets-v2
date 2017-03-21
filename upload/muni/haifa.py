from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class HaifaMuni(AbstractMuni):
    MUNI = 'haifa'
    def __init__(self,**kwargs):
        self.data_fields.add_value({0: CodeField,
              2: DescriptionField,
              7: AmountField},2016)
        self.start_in_row.add_value(1,year=2016)
        self.data_fields.add_value({0: CodeField,
              2: DescriptionField,
              4: AmountField},2015)
        self.start_in_row.add_value(1,year=2015)
        super(HaifaMuni,self).__init__(**kwargs)