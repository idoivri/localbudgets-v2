# -*- coding: utf-8 -*-
#!/usr/bin/env python

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse
from pymongo import MongoClient as client

from server.utils.utils import get_res

import itertools, random, json

results_keys = set()
results_dict = {}

def set_data():
    if results_keys:
        return

    random.seed(5042)

    for comb in itertools.permutations([10, 30,20,33]):
        key = '.'.join(str(_) for _ in comb)
        results_keys.add(key)
        results_dict[key] = {
            'muni' : 'hura',
            'year' : random.randint(2010,2015),
            'code' : key,
            'amount' : random.randint(1000,50000)
        }



@api_view(['GET'])
def api_index(request):
    """The entry endpoint of our v1 API"""

    return Response({
                        'lines': reverse('lines', request=request),
                        'get_query_result': reverse('get_query_result', request=request),
                        'get_autocomplete': reverse('autocomplete', request=request)
                    })

@api_view(['GET'])
def get_query_result(request):
    res = get_res(request)
    return Response({
        'commands' : ['lines'],

    })

@api_view(['GET'])
def get_autocomplete(request):
    q = request.GET.get('term', '')

    set_data()
    res = []
    for key_id,key in enumerate(results_keys):
        if key.startswith(q):
            res.append({'id':key_id,'label':'','value':json.dumps(results_dict[key])})


    return HttpResponse(json.dumps(res), 'application/json')
