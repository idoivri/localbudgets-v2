from rest_framework.decorators import api_view
# from rest_framework.reverse import reverse
from rest_framework.response import Response

from server.api.v1.utils.utils import get_res

@api_view(['GET'])
def api_v1(request):
    """The entry endpoint of our v1 API"""

    return Response({
        'commands' : ['lines'],

    })


@api_view(['GET'])
def get_query_result(request):
    res = get_res(request)
    return Response({
        'commands' : ['lines'],

    })
