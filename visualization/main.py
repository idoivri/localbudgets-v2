from django.core.management.base import BaseCommand

import os
import os.path
from os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module

import csv
from visualization.utils import Dataset as tree_Dataset
from visualization.utils import FlatenDataset as flaten_Dataset
from visualization.tree import Tree
from upload.utils import Dataset as raw_Dataset


SCHEME_FILENAME = 'data/schema/1994.csv'

class TreeCommand(BaseCommand):
    fields = ['CODE', 'PARENT', 'PARENT SCOPE', 'DIRECTION', 'INVERSE', 'INVERSE SCOPE', 'COMPARABLE', 'NAME', 'NAME_EN',
              'NAME_RU', 'NAME_AR', 'DESCRIPTION', 'DESCRIPTION_EN', 'DESCRIPTION_RU', 'DESCRIPTION_AR']
    def _parse_csv(self, filename):
        '''
        Parse the csv into a csv reader object.
        '''
        reader = csv.DictReader(file(filename, 'rb'), self.fields)
        #remove the header line
        reader.next()

        return reader
        
    def handle(self, *args, **options):
        print "bla for the win"
        reader = self._parse_csv(SCHEME_FILENAME)

        # Create all the nodes in a linear way. 
        # We Create dictionary in the following format
        # { node_code : [node_object, node_parent_code] }
        nodes = {line['CODE']: [Tree(name=line['NAME'],
                                     code=line['CODE']), 
                                line['PARENT']] 
                 for line in reader}
        root = Tree()

        # We go through the dict to create the hierarchy.
        for [node,parent] in nodes.values():
            if not parent:
                root.add_child(node)
            else:
                nodes[parent][0].add_child(node)

        # Upload the Tree to the DB.
        dataset = tree_Dataset('scheme', 0, clean=True)
        dataset.insert(root.to_dict())
        # bla = root.to_db(dataset)
        # dict = Tree.from_db(dataset,dataset.find_one({'_id':bla}))
        dataset.close()

        print dict

class Muni2TreeCommand(BaseCommand):
    def handle(self, *args, **options):
        muni = args[0]
        year = args[1]
        print "bla for the win"
        schema_datasset = tree_Dataset('scheme', 0)
        tree = Tree.from_dict(schema_datasset.find_one())
        tree.update_field('muni',muni)
        tree.update_field('year',year)
        raw_dataset = raw_Dataset(muni,year)
        for line in raw_dataset.find({}):
            node = Tree(muni=muni,year=year,**line)
            # import pdb; pdb.set_trace()
            tree.insert_node(node)
        tree.update_amount()
        dataset = tree_Dataset(muni,year, clean=True)
        dataset = flaten_Dataset('flaten')
        # dataset.insert(tree.to_dict())
        tree.to_db(dataset)

