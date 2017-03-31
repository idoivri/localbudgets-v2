from django.conf.urls import include, url
from django.views.generic import TemplateView
# from django.conf import settings
from django.contrib import admin
from server.api import urls as api_urls
from server import views as server_views



# This two if you want to enable the Django Admin: (recommended)
from django.contrib import admin
admin.autodiscover()


admin.autodiscover()

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    url(r'^$', server_views.index_page),
]
