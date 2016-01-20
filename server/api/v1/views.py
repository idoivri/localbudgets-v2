# -*- coding: utf-8 -*-
#!/usr/bin/env python

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse
from pymongo import MongoClient as client

from server.utils.utils import get_res
from server.utils import dumps
from server.models import get_munis as db_get_munis
from visualization.api import search_code
from visualization.api import get_budget_tree as vis_get_budget_tree
from visualization.api import get_node_subtree as vis_get_node_subtree
from visualization.api import get_budget as vis_get_budget

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
        res.append({'id':key_id,'label':'','value':dumps(results_dict[key])})


    # print res
    return HttpResponse(dumps(res), 'application/json')

@api_view(['GET'])
def get_budget_tree(request):
    muni = request.GET.get('muni')
    year = request.GET.get('year')
    layer = request.GET.get('layer', 1)
    return HttpResponse(dumps(vis_get_budget_tree(muni, year, layer)), 'application/json')

@api_view(['GET'])
def get_budget(request):
    muni = request.GET.get('muni', None)
    year = request.GET.get('year', None)
    # FIXME: the convert might be a bug
    layer = int(request.GET.get('layer', 1))
    return HttpResponse(dumps(vis_get_budget(muni, year, layer)), 'application/json')

@api_view(['GET'])
def get_node_subtree(request):
    node_id = request.GET.get('node_id', None)
    layer = int(request.GET.get('layer', 1))
    return HttpResponse(dumps(vis_get_node_subtree(node_id, layer)), 'application/json')


@api_view(['GET'])
def get_munis(request):
    munis = db_get_munis()
    munis = list(munis.find({}))

    return HttpResponse(dumps(munis, 'application/json'))
