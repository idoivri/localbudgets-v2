from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class HolonMuni(AbstractMuni):
    MUNI = 'holon'
    def __init__(self,**kwargs):
        super(HolonMuni, self).__init__(**kwargs)
        self.data_fields.add_value({0: CodeField,
              5: DescriptionField,
              10: AmountField},2014)
        self.start_in_row.add_value(2,year=2014)
        self.data_fields.add_value({0: CodeField,
              5: DescriptionField,
              9: AmountField},2015)
        self.start_in_row.add_value(2,year=2015)
        self.data_fields.add_value({0: CodeField,
              5: DescriptionField,
              8: AmountField},2016)
        self.start_in_row.add_value(2,year=2016)
