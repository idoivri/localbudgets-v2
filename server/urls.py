from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# from django.conf import settings
from django.contrib import admin
from server.api import urls as api_urls
from server import views as server_views
from visualization import views as vis_views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'budget.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_urls)),
    # url(r'^show_muni/(\w+)/(\d+)/$',server_views.show_table),
    url(r'^$', server_views.index_page), #TemplateView.as_view(template_name='index.html')
#    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^show_graph/(\w+)/$',vis_views.show_graph),
    url(r'^show_pie/(\w+)/(\d+)/$',vis_views.show_pie),
)
