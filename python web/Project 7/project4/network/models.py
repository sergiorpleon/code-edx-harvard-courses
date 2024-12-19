from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def number_of_following(self):
        total_following = 0
        for following in self.following.all():
            total_following += 1
        return total_following

    def number_of_followers(self):
        total_followers = 0
        for follower in self.followers.all():
            total_followers += 1
        return total_followers

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.content[:20]}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "content": self.content,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
        }

    def number_of_like(self):
        total_like = 0
        for like in self.likes.all():
            total_like += 1
        return total_like

    def user_like(self, user_id):

        for like in self.likes.all():
            if like.user.id == user_id:
                return True
        return False

class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} follor {self.followed_user.username}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "followed_user": self.followed_user.id,
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} like {self.post.content[:10]}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.id,
            "post": self.post.id,
        }
