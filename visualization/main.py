from django.core.management.base import BaseCommand

import os
import os.path
from os.path import join, extsep
from settings import BASE_DIR as root_dir
from importlib import import_module

import csv
from server.models import get_raw_budget,get_flatten, get_scheme,muni_iter, get_munis
from visualization.tree import Tree


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
        dataset = get_scheme()
        dataset.insert(root.to_dict())
        dataset.close()


class Muni2TreeCommand(BaseCommand):
    def handle(self, *args, **options):
        print "bla for the win"

        schema_datasset = get_scheme()
        flatten_dataset = get_flatten()
        for (muni,year) in muni_iter():
            print muni, year
            tree = Tree.from_dict(schema_datasset.find_one())
            tree.update_field('muni',muni)
            tree.update_field('year',year)
            budget_dataset = get_raw_budget(muni,year)
            for line in budget_dataset.find({}):
                node = Tree(muni=muni,year=year,**line)
                tree.insert_node(node)

            tree.update_amount()
            root = tree.to_db(flatten_dataset)
            update_root(muni,year,root)
            budget_dataset.close()

        schema_datasset.close()
        flatten_dataset.close()

def update_root(muni,year,root):
    munis=get_munis()
    entry = munis.find_one({'name':muni})
    if not 'roots' in entry.keys():
        entry['roots'] = {}
    entry['roots'][str(year)] = root
    munis.save(entry)
    munis.close()
