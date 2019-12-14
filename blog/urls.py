# from django.conf.urls import url
from django.contrib import admin
# from .views import *

from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),

    # url(r'^$', BlogsList.as_view(), name="blog-list"),
    # url(r'^create$', BlogsCreate.as_view(), name="blog-create"),
    # url(r'^simple_view$', view, name="just-view"),
]
