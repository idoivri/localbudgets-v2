from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from server.api.v1.views import api_index, get_budget_tree, get_munis,get_node_subtree,get_muni_roots


urlpatterns = [

    url(r'^$', api_index, name='api_v1'),
    url(r'^get_muni_roots', get_muni_roots, name="get_muni_roots"),
    url(r'^get_budget_tree', get_budget_tree, name="get_budget_tree"),
    url(r'^get_munis', get_munis, name="get_munis"),
    url(r'^get_node_subtree', get_node_subtree, name="get_node_subtree"),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
