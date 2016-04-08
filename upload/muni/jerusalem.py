from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField



class JerusalemMuni(AbstractMuni):
    fields = {2: CodeField,
              1: DescriptionField,
              0: AmountField}

    MUNI = 'jerusalem'

    info = {}
