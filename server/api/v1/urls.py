from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from server.api.v1.views import api_index, get_query_result, get_autocomplete, get_budget_tree, get_budget, get_munis,get_node_subtree,get_muni_roots


urlpatterns = [

    url(r'^$', api_index, name='api_v1'),
    url(r'get_query_result', get_query_result, name="get_query_result"),
    url(r'^get_autocomplete', get_autocomplete, name="autocomplete"),
    url(r'^get_muni_roots', get_muni_roots, name="get_muni_roots"),
    url(r'^get_budget_tree', get_budget_tree, name="get_budget_tree"),
    url(r'^get_budget', get_budget , name="get_budget"),
    url(r'^get_munis', get_munis , name="get_munis"),
    url(r'^get_node_subtree', get_node_subtree, name="get_node_subtree"),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
