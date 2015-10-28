from django.core.management.base import BaseCommand

import os
import os.path	
from  os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module
from server.models import get_munis
from upload.muni import munis_loaders

# TODO: maybe move this const to a module configuration file?
DATA_DIR = 'data'
SCHEMA = 'schema'

# TODO: add options


class NoMuniParser(Exception): pass 


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
        make_option('--clean_all',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean the DB before the Command'),
        )

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
            db.dataset.insert({'name':muni_object.MUNI,'info':muni_object.info,'years':years})
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
        years = []

        for filename in os.listdir(muni_path):
            # self.handle_sheet(muni_object, join(muni_path, filename))
            year = parse_filename(filename)
            muni_object.handle_sheet(year, join(muni_path, filename))
            years.append(year)

        self.add_muni(muni_object, years)


    def handle(self, *args, **options):
        print "bla for the win"
        # if options['clean']:
        #     del_collection(RAW_COLLECTION)
        muni_list = [muni for muni in os.listdir(join(root_dir, DATA_DIR)) if not muni==SCHEMA]
        if len(args) > 0:
            muni_list = filter(lambda x: x in muni_list,args)

        if len(muni_list) > 0:
            for muni in muni_list:
                self.handle_muni(muni, options)
