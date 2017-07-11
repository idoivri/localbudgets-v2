# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import csv
from server.models import get_raw_budget,get_flatten, get_scheme,muni_iter, get_munis,get_muni_years
from visualization.tree import Tree


SCHEME_FILENAME = 'data/schema/1994.csv'

class TreeCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean the DB before the Command')

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
        # get the db, exit if exists
        dataset = get_scheme()
        if dataset.count() > 0:
            if options['clean']:
                dataset.delete_many({})
            else:
                print 'Schema is already uploaded. Exiting.'
                return
        reader = self._parse_csv(SCHEME_FILENAME)
        # Create all the nodes in a linear way. 
        # We Create dictionary in the following format
        # { node_code : [node_object, node_parent_code] }
        nodes = {line['CODE']: [Tree(name=line['NAME'],
                                     code=line['CODE'],
                                     expense=line['DIRECTION']), 
                                line['PARENT']] 
                 for line in reader}
        root = Tree()

        expenditure_root = Tree(name=u'הוצאות', amount=None, code=None, expense=True, _id=None)
        revenue_root = Tree(name=u'הכנסות', amount=None,  code=None, expense=False, _id=None)
        root.add_child(expenditure_root)
        root.add_child(revenue_root)

        # We go through the dict to create the hierarchy.
        for [node, parent] in nodes.values():
            if not parent:
                if node.expense:
                    expenditure_root.add_child(node)
                else:
                    revenue_root.add_child(node)
            else:
                nodes[parent][0].add_child(node)

        # Upload the Tree to the DB.
        dataset.insert(root.to_dict())
        dataset.close()


class Muni2TreeCommand(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--print',
            action='store_true',
            dest='print_data',
            default=False,
            help='Print muni data to screen')
        parser.add_argument('--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean the DB before the Command')
        parser.add_argument('--muni',
            dest='muni',
            metavar="MUNI",
            help='Specify muni')
        parser.add_argument('--year',
            dest='year',
            default=None,
            metavar="YEAR",
            help='Specify year')



    def handle(self, *args, **options):
        print "bla for the win"
        flatten_dataset = get_flatten()
        for (muni, info) in muni_iter(**options):
            if options['year'] is not None:
                years = [options['year']]
            else:
                years = get_muni_years(muni)
            for year in years:
                print 'Converting to tree the budget %s of year %s'%(muni, year)

                if budget_exists(muni, year):
                    if options['clean']:
                        remove_muni_year_tree(muni, year)
                    else:
                        print "Budget %s, of year %s is already uploaded. Use clean to overwrite."%(muni,year)
                        continue
                tree = create_tree(muni,year)
                tree.name = "%s (%s)" %(info['heb_name'], year)
                root = tree.to_db(flatten_dataset)
                update_root(muni,year,root)

        flatten_dataset.close()

def budget_exists(muni,year):
    munis=get_munis()
    entry = munis.find_one({'name':muni})
    if not 'roots' in entry.keys():
        return False
    else:
        return (str(year) in entry['roots'].keys())

def remove_muni_year_tree(muni, year):
    print 'Cleaning budget tree of %s of year %s'%(muni, year)
    flatten = get_flatten()
    results = flatten.delete_many({'muni':muni,'year': year })
    flatten.close()

    munis = get_munis()
    entry = munis.find_one({'name':muni})

    entry['roots'].pop(str(year))
    munis.save(entry)
    munis.close()

def create_tree(muni, year):
    schema_dataset = get_scheme()

    tree = Tree.from_dict(schema_dataset.find_one())
    tree.update_field('muni', muni)
    tree.update_field('year', year)
    if tree.children[0].expense:
        expense_root = tree.children[0]
        revenue_root = tree.children[1]
    else:
        expense_root = tree.children[1]
        revenue_root = tree.children[0]

    budget_dataset = get_raw_budget(muni, year)

    for i, line in enumerate(budget_dataset.find({})):
        node = Tree(muni=muni, year=year, **line)
        if len([x for x in expense_root.children if x.code == node.code[1]]):
            expense_root.insert_node(node)
        else:
            revenue_root.insert_node(node)


    tree.update_amount()

    schema_dataset.close()
    budget_dataset.close()

    return tree

def update_root(muni,year,root):
    munis=get_munis()
    entry = munis.find_one({'name':muni})
    entry['roots'][str(year)] = root
    munis.save(entry)
    munis.close()

