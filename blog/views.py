from django.shortcuts import render, resolve_url
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.contrib.auth.models import User

from .models import Blog, Post
from .forms import *

def post_list(request):
    return render(request, 'blog/post_list.html', {})

def view(request):

    SUPER_STRING = "HELLO"

    return render(request, 'blog/view.html', {
        "LIST_OF_NUMBERS": [1,2,3],
        "SUPER_STRING": SUPER_STRING
        })


class BlogsView(DetailView):

    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blog'


from django.db.models import Q
from django.db.models import Count


class BlogsList(ListView):

    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs_list'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Blog.objects.filter(author=self.request.user)
        else:
            return Blog.objects.none()
        #return Blog.objects.filter(title='dd')
        #return Blog.objects.filter(author=self.request.user)
        #return Blog.objects.filter(Q(title__startswith='dd'))

    def get_context_data(self, **kwargs):
        context = super(BlogsList, self).get_context_data(**kwargs)

        import pandas as pd
        from collections import Counter

        context['all_blogs'] = Blog.objects.all()
        c = Counter()
        for blog in context['all_blogs']:
            c += Counter(blog.description)
        context['counter_l'] = pd.DataFrame.from_dict(c, orient='index').reset_index().to_html()

        # context['all_users'] = User.objects.all()
        context['all_users'] = User.objects.all().aggregate(Count('author'))
        #print(context['all_users'])
        return context


class BlogsCreate(CreateView):
    
    model = Blog
    form = BlogForm
    template_name = 'blog/blog_create.html' 
    fields = ('title', 'description')

    # def dispatch(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated():
    #         self.blog = self.request.user.blogger
    #     return super(PostsCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance.blog = self.blog
        return super(BlogsCreate, self).form_valid(form)

    def get_success_url(self):
        return resolve_url("blog-list")
