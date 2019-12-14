from django.conf.urls import url
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^$', BlogsList.as_view(), name="blog-list"),
    url(r'^create$', BlogsCreate.as_view(), name="blog-create"),
    url(r'^simple_view$', view, name="just-view"),
]
