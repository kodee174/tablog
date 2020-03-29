from django.contrib import admin
from .models import User, Post, Tag, Comment

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)