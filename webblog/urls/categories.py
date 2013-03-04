from django.conf.urls.defaults import *
from webblog.models import Category

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all()}, 'webblog_category_list' ),
    url(r'^(?P<slug>[-\w]+)/$', 'webblog.views.category_detail', {}, 'webblog_category_detail'),
    )
