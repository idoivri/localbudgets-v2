# -*- coding: utf-8 -*-
#!/usr/bin/env python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import logging


from server.models import get_muni_years


@api_view(['GET'])
def get_muni_year(request):
    if 'name' in request.GET:
        years = [year for year in get_muni_years(request.GET['name'])]
    else:
        years = []

    return Response(JSONRenderer().render({
        'res' : years,
    }))
