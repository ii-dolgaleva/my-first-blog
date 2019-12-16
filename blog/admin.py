from django.contrib import admin
from .models import Blog, Post, Comment

admin.site.register([Blog, Post, Comment])
