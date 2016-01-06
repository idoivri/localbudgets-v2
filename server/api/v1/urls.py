from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from server.api.v1.views import api_index, get_query_result, get_autocomplete, get_budget_tree, get_budget, get_munis
import server.api.v1.commands.commands as commands


urlpatterns = [

    url(r'^$', api_index, name='api_v1'),
    url(r'get_query_result', get_query_result, name="get_query_result"),
    url(r'^get_autocomplete', get_autocomplete, name="autocomplete"),
    url(r'^get_muni_year', commands.get_muni_year, name="get_muni_year"),
    url(r'^get_budget_tree', get_budget_tree , name="get_budget_tree"),
    url(r'^get_budget', get_budget , name="get_budget"),
    url(r'^get_munis', get_munis , name="get_munis"),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
