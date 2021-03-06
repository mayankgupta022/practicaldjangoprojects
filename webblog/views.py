from django.shortcuts import get_object_or_404,render_to_response
from webblog.models import Entry, Category
from django.template import Template, RequestContext

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('webblog/category_detail.html',
                              { 'object_list': category.live_entry_set(),
                                'title': category.title,
                                'description': category.description }, context_instance=RequestContext(request))