class AbstractMuni(object):
    """abstract municipality class"""
	
    def __init__(self, print_data=False):
        self.print_data = print_data
	
    def handle_sheet( self ):
        raise NotImplementedError( "Should have implemented handle_sheet in specific municipality" )