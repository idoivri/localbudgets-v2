from muni import AbstractMuni
from fields import AmountField, CodeField,CodeFieldAdd1, DescriptionField

class TelAvivMuni(AbstractMuni):
    MUNI = 'tel_aviv'
    def __init__(self,**kwargs):
        super(TelAvivMuni, self).__init__(**kwargs)
        self.data_fields.add_value({4: CodeFieldAdd1,
              6: DescriptionField,
              7: AmountField},2016)
        self.start_in_row.add_value(8,year=2016)
        self.data_fields.add_value({4: CodeFieldAdd1,
              6: DescriptionField,
              10: AmountField},2015)
        self.start_in_row.add_value(8,year=2015)
        self.data_fields.add_value({4: CodeFieldAdd1,
              6: DescriptionField,
              12: AmountField},2014)
        self.start_in_row.add_value(8,year=2014)
        self.data_fields.add_value({3: CodeField,
                                    4: DescriptionField,
                                    5: AmountField}, 2013)
        self.start_in_row.add_value(1, year=2013)
        self.data_fields.add_value({3: CodeField,
                                    4: DescriptionField,
                                    6: AmountField}, 2012)
        self.start_in_row.add_value(1, year=2012)
        self.data_fields.add_value({3: CodeField,
                                4: DescriptionField,
                                7: AmountField}, 2011)
        self.start_in_row.add_value(1, year=2011)


