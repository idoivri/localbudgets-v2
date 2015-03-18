# -*- coding: utf-8 -*-
#!/usr/bin/env python
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from pymongo import MongoClient as client
from rest_framework.renderers import JSONRenderer

_heb_convert = { u'hura':u"הופה היי" }

def find_term(term, line):
    return line['code'] == term or \
            term in line['name']

def get_heb_name(muni):
    return _heb_convert[muni]

def get_results_advanced(database, request):
    res = []

    year = request.GET['year']
    city = request.GET['city']
    query = request.GET['query']
    dbs = [name for name in database.collection_names() if "system" not in name]

    for name in dbs:
        if '.' not in name:
            continue

        muni_str, year_str = name.split('.')

        if year and str(year) != year_str:
            continue
        elif city and city!=muni_str:
            continue

        muni = database[muni_str]
        year_dataset = muni[year_str]

        for line in year_dataset.find():
            add_line = True

            if query:
                add_line = find_term(query, line)

            if add_line:
                res.append({
                    'muni' : get_heb_name(muni_str),
                    'year' : int(year_str),
                    'code' : line['code'],
                    'amount' : line['amount'],
                    'name' : line['name']

                })

    return res

def get_results_term(database, request):
    res = []

    dbs = [name for name in database.collection_names() if "system" not in name]

    for name in dbs:
        if '.' not in name:
            continue
        muni_str, year_str = name.split('.')

        muni = database[muni_str]
        year_dataset = muni[year_str]

        for line in year_dataset.find(): # amnt,code,name
            add_line = True

            if 'code' in request.GET:
                if line['code'] != request.GET['code']:
                    add_line = False

            if add_line and 'name' in request.GET:
                 if line['name'] != request.GET['name']:
                    add_line = False

            if add_line and 'term' in request.GET:
                add_line = find_term(request.GET['term'], line)

            if add_line:
                res.append({
                    'muni' : get_heb_name(muni_str),
                    'year' : int(year_str),
                    'code' : line['code'],
                    'amount' : line['amount'],
                    'name' : line['name']

                })

    return res

@api_view(['GET'])
def lines(request):
    """The entry endpoint of our v1 API"""
    database = client().database
    # import pdb
    # pdb.set_trace()
    if 'term' in request.GET:
        res = get_results_term(database,request)

    else:
        res = get_results_advanced(database,request)

    return Response(JSONRenderer().render({
        'res' : res,
    }))
