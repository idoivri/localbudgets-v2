from django.core.management.base import BaseCommand

import os
import os.path
from os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module

import csv
from visualization.utils import Tree, Dataset

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
        # We Create dictenery in the following format
        # { node_code : [node_object, node_parent_code] }
        nodes = {line['CODE']: [Tree(name=line['NAME'],
                                     code=line['CODE']), 
                                line['PARENT']] 
                 for line in reader}
        root = Tree()

        # We go through the dict to create the hiercy.
        for [node,parent] in nodes.values():
            if not parent:
                root.add_child(node)
            else:
                nodes[parent][0].add_child(node)

        # Upload the Tree to the DB.
        dataset = Dataset('scheme', 0, clean=False)
        dataset.insert(root.to_dict())
        dataset.close()

        print Tree.from_dict(root.to_dict())

# class DB2TreeCommand(BaseCommand):
#     def handle(self, *args, **options):
#         print "bla for the win"
#         dataset = Dataset('hura',2010)
#         for line in dataset.find:
#
#
#         reader = csv.DictReader(file(SCHEME_FILENAME, 'rb'), fields)
#         reader.next() #remove the header line
#         nodes = {line['CODE']: [Tree(name=line['NAME'],code=line['CODE']), line['PARENT']] for line in reader}
#         root = Tree()
#         for [node,parent] in nodes.values():
#             if not parent:
#                 root.add_child(node)
#             else:
#                 nodes[parent][0].add_child(node)
#
#         print root
