from django.core.management.base import BaseCommand

import os
import os.path
from os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module

import csv
from visualization.utils import Tree, Dataset

SCHEME_FILENAME = 'data/schema/1994.csv'
fields = ['CODE', 'PARENT', 'PARENT SCOPE', 'DIRECTION', 'INVERSE', 'INVERSE SCOPE', 'COMPARABLE', 'NAME', 'NAME_EN',
          'NAME_RU', 'NAME_AR', 'DESCRIPTION', 'DESCRIPTION_EN', 'DESCRIPTION_RU', 'DESCRIPTION_AR']

class TreeCommand(BaseCommand):
    def handle(self, *args, **options):
        print "bla for the win"
        reader = csv.DictReader(file(SCHEME_FILENAME, 'rb'), fields)
        reader.next() #remove the header line
        nodes = {line['CODE']: [Tree(name=line['NAME'],code=line['CODE']), line['PARENT']] for line in reader}
        root = Tree()
        for [node,parent] in nodes.values():
            if not parent:
                root.add_child(node)
            else:
                nodes[parent][0].add_child(node)

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