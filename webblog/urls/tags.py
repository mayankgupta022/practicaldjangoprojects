from django.conf.urls.defaults import *
from webblog.models import Entry, Link
from tagging.models import Tag


urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': Tag.objects.all(), 'template_name': 'webblog/tag_list.html'}, 'webblog_tag_list'),
    
    url(r'^entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', { 
        'queryset_or_model': Entry.live.all(), 'template_name': 'webblog/entries_by_tag.html'}, 'webblog_entry_archive_tag'),
    
    url(r'^links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', {
        'queryset_or_model': Link.objects.all(), 'template_name': 'webblog/links_by_tag.html'}, 'webblog_link_archive_tag'),
)