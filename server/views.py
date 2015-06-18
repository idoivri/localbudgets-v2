# -*- coding: utf-8 -*-
#!/usr/bin/env python
from pymongo import MongoClient
from pymongo import MongoClient as client
from django.shortcuts import render

from upload.utils import Dataset

def show_table(request, muni_name,year):
    client = MongoClient()
    db = client.database
    muni = Dataset(muni_name,year)
    lines = []
    for line in muni.find():
        lines.append(line)

    return render(request, 'simple_table.html', {'query_results':lines} )

def index_page(request):
    res = []

    muni1 = {}
    muni1['id'] = 2
    muni1['active'] = ''
    muni1['value'] = 'dynamic'
    muni1['heb_name'] = u'בזרימה'
    res.append(muni1)

    muni = {}
    muni['id'] = 1
    muni['active'] = 'active'
    muni['value'] = 'standard'
    muni['heb_name'] = u'חיפוש רגיל'
    res.append(muni)

    return render(request,'index.html', {'munis_result':res})
