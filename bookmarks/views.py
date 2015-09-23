#Debugging
import sys
#Django Imports
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import logout
from bookmarks.forms import *
from django.views.generic import TemplateView
from bookmarks.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


#Switch all views to classes if i can find the time

# Browsing views

class MainPage(TemplateView):
    """Default view for the main page"""
    template_name = 'bookmarks/main_page.html'

def user_page(request, username):
    """View to display a users bookmarks"""
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmark_set.order_by('-id')
    template = 'bookmarks/user_page.html'
    context = RequestContext(request, {
        'username': username,
        'bookmarks': bookmarks,
        'show_description': True,
        'show_edit': username == request.user.username,
    })
    return render(request, template, context)

def search_page(request):
    """View for searching bookmarks"""
    form = SearchForm()
    bookmarks = []
    show_results = False
    if request.GET.has_key('query'):
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query': query})
            desc_search = Bookmark.objects.filter(description__icontains=query)
            title_search = Bookmark.objects.filter(title__icontains=query)
            bookmarks = (desc_search|title_search)[:10]
    context = RequestContext(request, {
        'form': form,
        'bookmarks': bookmarks,
        'show_results': show_results,
        'show_description': True,
    })
    return render_to_response('bookmarks/search.html', context)

# Session Management Views

def logout_page(request):
    """View to logout user"""
    logout(request)
    return HttpResponseRedirect('/bookmarks/')

def register_page(request):
    """View for user registration page"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/bookmarks/register/success')
    else:
        form = RegistrationForm()
    context = RequestContext(request, {
        'form':form
    })
    template = 'registration/register.html'
    return render_to_response(template, context)

class RegisterSuccessPage(TemplateView):
    """View for successful registration"""
    template_name = 'registration/register_success.html'


#Account Management Views

def _delete_page(request, url):
    """Deletes Bookmark and attached Link"""
    try:
        #find bookmark and link
        link = Link.objects.get(url=url)
        bookmark = Bookmark.objects.get(
            link=link,
            user=request.user
        )
        #delete bookmark
        bookmark.delete()
        #delete link if it is no longer referenced
        if link.bookmark_set.all().count()==0:
            link.delete()
    except ObjectDoesNotExist:
        pass

@login_required
def bookmark_delete_page(request):
    """View to delete a bookmark"""
    if request.GET.has_key('url'):
        url = request.GET['url']
        _delete_page(request, url)
    return HttpResponseRedirect('/bookmarks/user/%s'%request.user.username)

def _bookmark_save(request, form):
    """Saves a bookmark. Creates a new bookmark if the link is new"""
    # Create/get link.
    link, dummy = \
        Link.objects.get_or_create(url=form.cleaned_data['url'])
    # Create/get bookmark.
    try:
        print >> sys.stderr, 'Find bookmark...'
        bookmark = Bookmark.objects.get(
            user=request.user,
            link=link
        )
        bookmark.link=link
    except ObjectDoesNotExist:
        print >> sys.stderr, 'Bookmark not found'
        bookmark = Bookmark(
            user=request.user,
            link=link)
    # Update bookmark title.
    bookmark.title = form.cleaned_data['title']
    description = form.cleaned_data['description']
    bookmark.description = description
    # Save bookmark to database and return it.
    bookmark.save()
    return bookmark

@login_required
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
            return HttpResponseRedirect(
                '/bookmarks/user/%s/' % request.user.username
            )
    elif request.GET.has_key('url'):
        url = request.GET['url']
        title = ''
        description = ''
        try:
            link = Link.objects.get(url=url)
            bookmark = Bookmark.objects.get(
                link=link,
                user=request.user
            )
            title = bookmark.title
            description = bookmark.description
        except ObjectDoesNotExist:
            pass
        form = BookmarkSaveForm({
            'url': url,
            'title': title,
            'description': description,
        })
    else:
        form = BookmarkSaveForm()
    context = RequestContext(request, {
        'form': form
    })
    return render_to_response('bookmarks/bookmark_save.html', context)