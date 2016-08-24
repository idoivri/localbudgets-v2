from django.core.management.base import BaseCommand

import os
import os.path	
from  os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module
from server.models import get_munis, del_database
from upload.muni import munis_loaders


# TODO: maybe move this const to a module configuration file?
DATA_DIR = 'data'
SCHEMA = 'schema'

# TODO: add options


class NoMuniParser(Exception): pass 


def parse_filename(filename):
    try:
        year_str, ext = os.path.basename(filename).split(extsep)
    except ValueError: #File is not in the format of *.*
        print 'file name ({}) should be in format yyyy.csv'.format(filename)
        return None
    try:
        year = int(year_str)
    except ValueError: #File is not in the format of *.*
        print 'file name ({}) should be in format yyyy.csv'.format(filename)
        return None
    if not 1900<year<2100:
        print 'file name ({}) should be in format yyyy.csv (1900<yyyy<2100)'.format(filename)
        return None
    return year

    
class UpdateCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--print',
            action='store_true',
            dest='print_data',
            default=False,
            help='Print muni data to screen')

        parser.add_argument('--clean_all',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean the DB before the Command'),

        parser.add_argument('--muni',
            dest='muni',
            help='Specify which muni to upload (otherwise all)'),

        parser.add_argument('--year',
            dest='year',
            help='Specify which year to upload (otherwise all)'),


    # def handle_sheet(self, muni_object, filepath):
    #     '''
    #     handle each csv file in the muni directory
    #     '''
    #     year = parse_filename(filepath)
    #     muni_object.handle_sheet(year, filepath)

    def add_muni(self,muni_object, years=None):
        db = get_munis()
        muni_entry = db.dataset.find_one({'name':muni_object.MUNI})

        if years is None:
            years = []

        if muni_entry is None:
            db.dataset.insert({'name':muni_object.MUNI,'info':muni_object.info,'years':years,'roots':{}})
        else:
            # import pdb; pdb.set_trace()
            muni_entry['years'] = list(set(muni_entry['years']+years))
            db.dataset.save(muni_entry)


    def handle_muni(self, muni, options):
        '''
        handle each muni in the root/data directory
        '''
        self.stdout.write("handling %s\n" %(muni, ))
        muni_path = join(root_dir, DATA_DIR, muni)
        if (muni in munis_loaders):
            muni_class = munis_loaders[muni]
        else:
            raise NoMuniParser("no Muni parser for: %s" %(muni, ))
        muni_object = muni_class(print_data=options['print_data'],clean=options['clean'])
        os.listdir(muni_path)
        years = {parse_filename(filename): filename for filename in os.listdir(muni_path) if parse_filename(filename) is not None}

        print years
        if options['year']:
            if int(options['year']) in years.keys():
                years = {int(options['year']): years[int(options['year'])]}
            else:
                print 'The budget for muni %s year %d does not exist '%(muni,int(options['year']))
                return

        for (year,filename) in years.items():
            muni_object.handle_sheet(year, join(muni_path, filename))

        self.add_muni(muni_object, years.keys())


    def handle(self, *args, **options):
        print "bla for the win"
        # if options['clean']:
        #     del_collection(RAW_COLLECTION)
        muni_list = [muni for muni in os.listdir(join(root_dir, DATA_DIR))
                     if (os.path.isdir(join(root_dir,DATA_DIR,muni)) and not muni==SCHEMA)]
        if options['muni']:
            if options['muni'] in muni_list:
                muni_list = [options['muni']]
            else:
                print 'Data for muni %s does not exist'%options['muni']
                return

        if len(muni_list) > 0:
            for muni in muni_list:
                self.handle_muni(muni, options)
                

class CleanCommand(BaseCommand):
    def handle(self, *args, **options):
        del_database()
