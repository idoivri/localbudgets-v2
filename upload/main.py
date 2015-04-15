from django.core.management.base import BaseCommand

import os
import os.path
from  os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module

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
    def handle_sheet(self, muni_module, filepath):
        '''
        handle each csv file in the muni directory
        '''
        year = parse_filename(filepath)
        muni_module.handle_sheet(year, filepath)
        
         
    def handle_muni(self, muni):
        '''
        handle each muni in the root/data directory
        '''
        self.stdout.write("handling %s\n" %(muni, ))
        muni_path = join(root_dir, DATA_DIR, muni)
        muni_module = import_muni_module(muni)
        
        for filename in os.listdir(muni_path):
            self.handle_sheet(muni_module, join(muni_path, filename))
        

    def handle(self, *args, **options):
        print "bla for the win"
        for muni in os.listdir(join(root_dir, DATA_DIR)):
            self.handle_muni(muni)
