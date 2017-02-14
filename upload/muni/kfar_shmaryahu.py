from muni import AbstractMuni

class KfarShmaryahuMuni(AbstractMuni):
    MUNI = 'kfar_shmaryahu'

    def handle_sheet(*args):
        # TODO
        pass

    def __init__(self,**kwargs):
        self.start_in_row.add_value(3)
        super(KfarShmaryahuMuni, self).__init__(**kwargs)