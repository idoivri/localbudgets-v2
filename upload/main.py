from django.core.management.base import BaseCommand

import os
import os.path	
from  os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module
from server.models import del_collection

# TODO: maybe move this const to a module configuration file?
DATA_DIR = 'data'

# TODO: add options

MUNI_MODULES_PREFIX = "upload.muni."


class NoMuniParser(Exception): pass 

# try to import the right handler for the current muni
def import_muni_module(muni):
    try:
        muni_module = import_module(MUNI_MODULES_PREFIX + muni)
    except Exception,e:
        raise NoMuniParser("No Plugin for %s or error: %s" % (muni, str(e)))

    return muni_module
    

def parse_filename(filename):
    year_str, ext = os.path.basename(filename).split(extsep)
    return int(year_str)

    
class UpdateCommand(BaseCommand):

    from optparse import make_option
    option_list = BaseCommand.option_list + (
        make_option('--print',
            action='store_true',
            dest='print_data',
            default=False,
            help='Print muni data to screen'),
        make_option('--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean the DB before the Command'),
        )

    def handle_sheet(self, muni_object, filepath):
        '''
        handle each csv file in the muni directory
        '''
        year = parse_filename(filepath)
        muni_object.handle_sheet(year, filepath)
        
         
    def handle_muni(self, muni, options):
        '''
        handle each muni in the root/data directory
        '''
        self.stdout.write("handling %s\n" %(muni, ))
        muni_path = join(root_dir, DATA_DIR, muni)
        muni_module = import_muni_module(muni)
        muni_class = getattr(muni_module, 'Muni')
        muni_object = muni_class(print_data=options['print_data'])
        
        for filename in os.listdir(muni_path):
            self.handle_sheet(muni_object, join(muni_path, filename))
        

    def handle(self, *args, **options):
        print "bla for the win"

        if options['clean']:
            del_collection('raw')

        muni_list = os.listdir(join(root_dir, DATA_DIR))
        if len(args) > 0:
            muni_list = filter(lambda x: x in muni_list,args)

        if len(muni_list) > 0:
            for muni in muni_list:
                self.handle_muni(muni, options)
