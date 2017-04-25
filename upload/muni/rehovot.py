from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RehovotMuni(AbstractMuni):
    MUNI = 'rehovot'
    def __init__(self,**kwargs):
        super(RehovotMuni, self).__init__(**kwargs)
        self.data_fields.add_value({1: CodeField,
              4: DescriptionField,
              8: AmountField},2016)
        self.start_in_row.add_value(2,year=2016)
        self.data_fields.add_value({1: CodeField,
              4: DescriptionField,
              7: AmountField},2015)
        self.start_in_row.add_value(2, year=2015)
        self.data_fields.add_value({0: CodeField,
              4: DescriptionField,
              6: AmountField},2014)
        self.start_in_row.add_value(98, year=2014)
        self.data_fields.add_value({0: CodeField,
              4: DescriptionField,
              5: AmountField},2013)
        self.start_in_row.add_value(98, year=2013)
        self.data_fields.add_value({0: CodeField,
              4: DescriptionField,
              7: AmountField},2012)
        self.start_in_row.add_value(95, year=2012)
        self.data_fields.add_value({0: CodeField,
              4: DescriptionField,
              6: AmountField},2011)
        self.start_in_row.add_value(95, year=2011)
