from django.core.management.base import BaseCommand

import os
from  os.path import join
from settings import BASE_DIR as root_dir

# TODO: maybe move this const to a module configuration file?
DATA_DIR = 'data'

class UpdateCommand(BaseCommand):

    def handle_sheet(self, ):
        '''
        handle each csv file in the muni directory
        '''
        pass

    def handle_muni(self, muni):
        '''
        handle each muni in the root/data directory
        '''
        print "handling %s" %(muni, )
        muni_path = join(root_dir, DATA_DIR, muni)

    def handle(self, *args, **options):
        print "bla for the win"
        for muni in os.listdir(join(root_dir, DATA_DIR)):
            self.handle_muni(muni)
