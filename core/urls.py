from django.conf.urls import url
from django.contrib import admin
from .views import *


urlpatterns = [
    
    url(r'^current_time$', show_current_time, name="current-time"),
]

