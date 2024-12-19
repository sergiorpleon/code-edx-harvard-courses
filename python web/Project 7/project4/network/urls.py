
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following/<int:user_id>", views.following, name="following"),

    path("posts/<int:post_id>", views.edit_post, name="edit_post"),

    path("like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("follow/<int:user_id>", views.toggle_follow, name="toggle_follow"),

    path("error>", views.error, name="error"),
    

]
