# -*- coding: utf-8 -*-
#!/usr/bin/env python

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse
from pymongo import MongoClient as client

from server.utils.utils import get_res
from visualization.api import search_code

import itertools, random, json

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
    results = search_code(q)
    results_dict = {tree['code']: tree for tree in results}
    results_keys = results_dict.keys()

    res = []
    for key_id,key in enumerate(results_keys):
        print results_dict[key]
        res.append({'id':key_id,'label':'','value':json.dumps(results_dict[key])})


    # print res
    return HttpResponse(json.dumps(res), 'application/json')
