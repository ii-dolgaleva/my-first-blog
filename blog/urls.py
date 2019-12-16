# from django.conf.urls import url
from django.contrib import admin
# from .views import *

from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),

    # url(r'^$', BlogsList.as_view(), name="blog-list"),
    # url(r'^create$', BlogsCreate.as_view(), name="blog-create"),
    # url(r'^simple_view$', view, name="just-view"),
]
