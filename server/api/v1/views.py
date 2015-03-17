from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_v1(request):
    """The entry endpoint of our v1 API"""

    return Response({
        # # TODO: Absolutely must be private! This endpoint exposes user data!

        'commands' : ['lines'],

    })
