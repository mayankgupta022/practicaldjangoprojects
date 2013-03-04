from django.conf.urls.defaults import *
import os
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^cms/', include('cms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':'media/'}),
    url(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': os.path.abspath("./tiny_mce")}),
    url(r'^webblog/categories/', include('webblog.urls.categories')),
    url(r'^webblog/links/', include('webblog.urls.links')),
    url(r'^webblog/tags/', include('webblog.urls.tags')),
    url(r'^webblog/feeds/', include('webblog.urls.feeds')),
    url(r'^webblog/', include('webblog.urls.entries')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    (r'^search/$', 'search.views.search'),
    #url(r'', include('django.contrib.flatpages.urls')),
)
