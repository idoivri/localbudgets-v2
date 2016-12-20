from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField


class KfarSabaMuni(AbstractMuni):
    MUNI = 'kfar_saba'

    fields = {0: CodeField,
              1: DescriptionField,
              8: AmountField}
