from muni import AbstractMuni

class SchemaMuni(AbstractMuni):
    MUNI = 'schema'
    info = {}

    def handle_sheet(*args):
        pass
    def __init__(self,**kwargs):
        self.start_in_row.add_value(3)
        super(SchemaMuni, self).__init__(**kwargs)