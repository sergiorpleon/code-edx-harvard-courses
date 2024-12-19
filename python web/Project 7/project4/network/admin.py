from django.contrib import admin
from .models import Post, Follower, Like, User
#from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(Like)
admin.site.register(User)
