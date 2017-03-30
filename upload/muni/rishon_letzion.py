from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class RishonLetzionMuni(AbstractMuni):

    fields = {0: CodeField,
              1: DescriptionField,
              4: AmountField}

    fields_2016 = {0: CodeField,
                  1: DescriptionField,
                  2: AmountField}
    fields_2015 = {0: CodeField,
                  1: DescriptionField,
                  3: AmountField}
    fields_2014 = {0: CodeField,
                  1: DescriptionField,
                  5: AmountField}

    years = {2012: fields,
             2013: fields,
             2014: fields_2014,
             2015: fields_2015,
             2016: fields_2016}

    MUNI = 'rishon_letzion'
    info = {}

    def __init__(self,**kwargs):
        super(RishonLetzionMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(3)

