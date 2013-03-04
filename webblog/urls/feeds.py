from django.conf.urls.defaults import *
from webblog.feeds import LatestEntriesFeed, CategoryFeed, LatestLinksFeed

urlpatterns = patterns('',
                       (r'^entries/$', LatestEntriesFeed()),
                       (r'^links/$', LatestLinksFeed()),
                       (r'^categories/$', CategoryFeed()),
)