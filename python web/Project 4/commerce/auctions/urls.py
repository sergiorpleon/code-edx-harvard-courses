from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("whatchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.listings_category, name="listings_category"),
    path("error", views.error, name="error"),
    
    path("add_whatchlist/<int:id>", views.add_whatchlist, name="add_whatchlist"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    
]
