# -*- coding: utf-8 -*-
#!/usr/bin/env python
from pymongo import MongoClient
from pymongo import MongoClient as client
from django.shortcuts import render

from server.models import get_budget, get_muni_names, muni_iter

from collections import defaultdict

from server.models import get_raw_budget

def index_page(request):

    res = defaultdict(list)
    for muni,year in muni_iter():
        res[muni].append(year)

    for muni in res:
        res[muni].sort()

    # res = [muni for muni in get_muni_names()]

    return render(request,'index.html', {'munis': res.keys(), 'muni_years' : res })
