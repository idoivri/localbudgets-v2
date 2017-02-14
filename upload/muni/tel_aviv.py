from muni import AbstractMuni

class TelAvivMuni(AbstractMuni):
    MUNI = 'tel_aviv'
    info = {}

    def handle_sheet(*args):
        pass
    def __init__(self,**kwargs):
        self.start_in_row.add_value(3)
        super(TelAvivMuni, self).__init__(**kwargs)