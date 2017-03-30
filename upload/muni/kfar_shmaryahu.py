from muni import AbstractMuni

class KfarShmaryahuMuni(AbstractMuni):
    MUNI = 'kfar_shmaryahu'

    def handle_sheet(*args):
        # TODO
        pass

    def __init__(self,**kwargs):
        super(KfarShmaryahuMuni, self).__init__(**kwargs)
        self.start_in_row.add_value(3)
