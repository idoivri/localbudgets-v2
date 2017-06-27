from muni import AbstractMuni
from fields import AmountField, CodeField, DescriptionField

class KfarShmaryahuMuni(AbstractMuni):
    MUNI = 'kfar_shmaryahu'
    def __init__(self, **kwargs):
        super(KfarShmaryahuMuni, self).__init__(**kwargs)
        self.data_fields.add_value({0: CodeField,
                                    2: DescriptionField,
                                    6: AmountField})
        self.start_in_row.add_value(1)


