from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from pymongo import MongoClient as client


@api_view(['GET'])
def lines(request):
    """The entry endpoint of our v1 API"""
    database = client().database
    res = []
    for line in database.hura.find(): # amnt,code,name
        add_line = True

        if 'code' in request.GET:
            if line['code'] != request.GET['code']:
                add_line = False

        if add_line and 'name' in request.GET:
             if line['name'] != request.GET['name']:
                add_line = False

        if add_line:
            res.append({
                'code' : line['code'],
                'amount' : line['amount'],
                'name' : line['name']

            })

    return Response({
        'res' : res,
    })
