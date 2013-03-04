import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from tagging.fields import TagField, Tag
import tagging
from markdown import markdown
from django.contrib.comments.models import Comment
from django.db.models import signals

class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    description = models.TextField()
    
    def live_entry_set(self):
        from webblog.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return ('webblog_category_detail', (), { 'slug': self.slug })
    
    get_absolute_url = models.permalink(get_absolute_url)

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique_for_date='pub_date', help_text="Suggested value automatically generated from title. Must be unique for the day.")
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    categories = models.ManyToManyField(Category)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    tags = TagField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    
    objects = models.Manager()
    live = LiveEntryManager()
    
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        super(Entry, self).save(force_insert, force_update)
    
    def get_absolute_url(self):
        return ('webblog_entry_detail', (), { 'year': self.pub_date.strftime("%Y"),
        'month': self.pub_date.strftime("%b").lower(),
        'day': self.pub_date.strftime("%d"),
        'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

tagging.register(Entry, tag_descriptor_attr='etags')

class Link(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    url = models.URLField(unique=True)
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    tags = TagField()
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text='The name of the person whose site you spotted the link on. Optional.')
    via_url = models.URLField('Via URL', blank=True, 
                              help_text='The URL of the site where you spotted the link. Optional.')
    
    class Meta:
        ordering = ['-pub_date']
        
    def __unicode__(self):
        return self.title
    
    def save(self):
        if not self.id and self.post_elsewhere:
            import pydelicious
            from django.utils.encoding import smart_str
            pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
                            smart_str(self.url), smart_str(self.title),
                            smart_str(self.tags))
        super(Link, self).save()
        
    def get_absolute_url(self):
        return ('webblog_link_detail', (), { 'year': self.pub_date.strftime('%Y'),
                                             'month': self.pub_date.strftime('%b').lower(),
                                             'day': self.pub_date.strftime('%d'),
                                             'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)
    
tagging.register(Link, tag_descriptor_attr='etags')


from akismet import Akismet
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

class EntryModerator(CommentModerator):
    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True
    
    def moderate (self, comment, content_object, request):
        already_moderated = super(EntryModerator, self).moderate(comment, content_object, request)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http:/%s/" %Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                             'referrer': request.META['HTTP_REFERER'],
                             'user_ip': comment.ip_address,
                             'user-agent': request.META['HTTP_USER_AGENT'] }
            return akismet_api.comment_check(smart_str(comment.comment),
                                akismet_data,
                                build_data=True)
        return False
        
moderator.register(Entry, EntryModerator)