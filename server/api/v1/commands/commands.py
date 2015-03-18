from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from pymongo import MongoClient as client
from rest_framework.renderers import JSONRenderer

def find_term(term, line):
    return line['code'] == term or \
            term in line['name']

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

        if 'term' in request.GET:
            add_line = find_term(request.GET['term'], line)

        if add_line:
            res.append({
                'code' : line['code'],
                'amount' : line['amount'],
                'name' : line['name']

            })

    return Response(JSONRenderer().render({
        'res' : res,
    }))
