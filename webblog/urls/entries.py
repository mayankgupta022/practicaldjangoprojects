from django.conf.urls.defaults import *
from webblog.models import Entry

entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
    }

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$', 'archive_index', entry_info_dict, name='webblog_entry_archive_index'),
    url(r'^(?P<year>\d{4})/$', 'archive_year', entry_info_dict, name='webblog_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', entry_info_dict, name='webblog_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', entry_info_dict, name='webblog_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', entry_info_dict, 'webblog_entry_detail'),
    )
