# -*- coding: utf-8 -*-
#!/usr/bin/env python

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse

from server.utils import dumps
from server.models import get_munis as db_get_munis
from server.models import get_muni_roots as db_get_muni_roots
from visualization.api import get_budget_tree as vis_get_budget_tree


@api_view(['GET'])
def api_index(request):
    """The entry endpoint of our v1 API"""

    return Response({
                        'get_muni_roots': reverse('get_muni_roots',request=request),
                        'get_budget_tree': reverse('get_budget_tree',request=request),
                        'get_munis': reverse('get_munis',request=request),
                        'get_node_subtree': reverse('get_node_subtree',request=request),
                    })

@api_view(['GET'])
def get_budget_tree(request):
    muni = request.GET.get('muni')
    year = request.GET.get('year')
    layer = request.GET.get('layer', 1000)
    expense = request.GET.get('expense', None)
    if expense is not None:
        if expense == 'true':
            expense = True
        elif expense == 'false':
            expense = False
        else:
            expense = None

    return HttpResponse(dumps(vis_get_budget_tree(muni, year, layer=layer, expense=expense)), 'application/json')

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

@api_view(['GET'])
def get_muni_roots(request):
    if 'name' in request.GET:
        years = sorted([year for year in db_get_muni_roots(request.GET['name'])])
    else:
        years = []

    return Response(JSONRenderer().render({
        'res': years,
    }))
