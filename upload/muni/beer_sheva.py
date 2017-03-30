from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class BeerMuni(AbstractMuni):

    fields_old = {10: CodeField,
                  11: DescriptionField,
                  15: AmountField}

    fields_2013 = {0: CodeField,
                  1: DescriptionField,
                  3: AmountField}
    fields_2016 = {0: CodeField,
                   1: DescriptionField,
                   5: AmountField}
    fields = {0: CodeField,
              1: DescriptionField,
              4: AmountField}

    years = {2011: fields_old,
             2012: fields_old,
             2013: fields_2013,
             2016: fields_2016}
    
    MUNI = 'beer_sheva'

    def __init__(self,**kwargs):
        super(BeerMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(0)
        self.start_in_row.add_value(1, year=2016)