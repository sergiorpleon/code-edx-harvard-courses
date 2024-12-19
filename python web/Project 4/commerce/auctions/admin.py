from django.contrib import admin
from .models import Category, Listing, Bid, Comment, Watchlist, User
#from django.contrib.auth.models import User


# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(User)