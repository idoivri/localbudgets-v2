from muni import AbstractMuni

class GushMuni(AbstractMuni):
    MUNI = 'gush_etzion'

    def handle_sheet(self, *args):
        # TODO
        pass

    def __init__(self,**kwargs):
        super(GushMuni, self).__init__(**kwargs)