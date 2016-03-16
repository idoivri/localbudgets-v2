from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# from django.conf import settings
from django.contrib import admin
from server.api import urls as api_urls
from server import views as server_views


admin.autodiscover()

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    # url(r'^show_muni/(\w+)/(\d+)/$',server_views.show_table),
    url(r'^$', server_views.index_page), #TemplateView.as_view(template_name='index.html')
    # url(r'^bubbles$', server_views.bubbles_index_page),
]
