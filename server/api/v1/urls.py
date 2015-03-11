from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from server.api.v1.views import api_v1


urlpatterns = [

    url(r'^$', api_v1, name='api_v1'),

#    url(r'^entities/', include(entities())),

#    url(r'^divisions/', include(divisions())),

#    url(r'^domains/', include(domains())),

#    url(r'^templates/', include(templates())),

#    url(r'^sheets/', include(sheets())),

#    url(r'^contexts/', include(contexts())),

#    url(r'^coefficients/', include(coefficients())),

#    url(r'^tools/', include(tool_urls)),

#    url(r'^accounts/', include(account_urls)),

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])
