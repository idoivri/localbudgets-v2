from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from server.api.v1.views import api_v1, get_query_result
import server.api.v1.commands.commands as commands


urlpatterns = [

    url(r'^$', api_v1, name='api_v1'),
    url(r'get_query_result', get_query_result),
    url(r'^lines', commands.lines),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
