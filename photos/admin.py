from django.contrib import admin
from .models import User, Post, Category

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)

