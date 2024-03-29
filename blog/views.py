from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from .models import Blog, Post, Comment

from .forms import *
# from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.pub_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.pub_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(pub_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


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
