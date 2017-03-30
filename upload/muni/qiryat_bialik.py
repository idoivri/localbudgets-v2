from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class QiryatBialikMuni(AbstractMuni):
    fields = {0: CodeField,
              1: DescriptionField,
              2: AmountField}  # TODO: make sure this is the right column number.

    MUNI = 'qiryat_bialik'
    info = {}
    def __init__(self,**kwargs):
        super(QiryatBialikMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(3)
