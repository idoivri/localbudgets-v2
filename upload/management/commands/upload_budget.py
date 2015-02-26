from django.core.management.base import BaseCommand
from settings import BASE_DIR as root_dir
import os
from  os.path import join

DATA_DIR = 'data'


class Command(BaseCommand):

    def handle_sheet(self,):
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
        
    def handle(self, *args, **kws):
        '''
        runs when we run "python manage.py upload_buget"
        '''
        print "bla for the win"
        for muni in os.listdir(join(root_dir, DATA_DIR)):
            self.handle_muni(muni)


