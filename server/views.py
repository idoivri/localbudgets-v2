# -*- coding: utf-8 -*-
#!/usr/bin/env python
from pymongo import MongoClient
from pymongo import MongoClient as client
from django.shortcuts import render

from server.models import get_muni_names, muni_iter

from collections import defaultdict

from server.models import get_raw_budget

def index_page(request):

    res = [(muni[0],muni[1]) for muni in get_muni_names()]
    return render(request,'index.html', {'munis': res})

def bubbles_index_page(request):
	return render(request,'bubbles_index.html')
