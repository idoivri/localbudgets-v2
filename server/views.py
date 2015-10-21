# -*- coding: utf-8 -*-
#!/usr/bin/env python
from pymongo import MongoClient
from pymongo import MongoClient as client
from django.shortcuts import render

from server.models import get_budget, get_muni_names

from collections import defaultdict

from server.models import get_raw_budget

def show_table(request, muni_name,year):
    # client = MongoClient()
    # db = client.database
    muni = get_raw_budget(muni_name,year)
    lines = []
    for line in muni.find():
        lines.append(line)

    muni.close()
    return render(request, 'simple_table.html', {'query_results':lines} )

# def

def index_page(request):
    # res = []
    #
    # muni1 = {}
    # muni1['id'] = 2
    # muni1['active'] = ''
    # muni1['value'] = 'dynamic'
    # muni1['heb_name'] = u'בזרימה'
    # res.append(muni1)
    #
    # muni = {}
    # muni['id'] = 1
    # muni['active'] = 'active'
    # muni['value'] = 'standard'
    # muni['heb_name'] = u'חיפוש רגיל'
    # res.append(muni)
    # client = muni_

    # res = defaultdict(list)
    # for muni,year in muni_iter():
    #     res[muni].append(year)
    #
    # for muni in res:
    #     res[muni].sort()

    res = [muni for muni in get_muni_names()]

    # muni.close()
    return render(request,'index.html', {'munis': res})
