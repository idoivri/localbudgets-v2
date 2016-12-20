from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class NetanyaMuni(AbstractMuni):

    fields_2016 = {0: CodeField,
                  1: DescriptionField,
                  2: AmountField}

    fields_2015 = {0: CodeField,
                  1: DescriptionField,
                  3: AmountField}
    fields_2014 = {0: CodeField,
              1: DescriptionField,
              4: AmountField}

    years = {2016: fields_2016,
             2015: fields_2015,
             2014: fields_2014}
    
    MUNI = 'netanya'

