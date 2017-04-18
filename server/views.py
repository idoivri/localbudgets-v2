# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render

from server.models import get_muni_names


def index_page(request):

    res = [(muni[0],muni[1]) for muni in get_muni_names(only_with_years=True)]
    
    return render(request, 'index.html', {'munis': res})

def bubbles_index_page(request):
	return render(request,'bubbles_index.html')
