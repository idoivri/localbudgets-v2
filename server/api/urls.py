from django.conf.urls import include, url
from server.api.v1 import urls as v1_urls
from server.api.views import api_index

urlpatterns = [
    url(r'^$', api_index, name='api'),
    url(r'^v1/', include(v1_urls),),
    ]
