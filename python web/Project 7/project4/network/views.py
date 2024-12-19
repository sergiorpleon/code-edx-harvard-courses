import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follower, Like


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def index(request):
        #Get all post
        all_posts = Post.objects.all().order_by('-created_at')
        form = PostForm()
        
        #If user is login check if form is valid and add user
        if request.method == "POST":
            if(request.user.id):
                form = PostForm(request.POST)
                if form.is_valid():
                    form.save(commit=False)
                    form.instance.user = request.user
                    form.save()
                    form = PostForm()
                    return HttpResponseRedirect("/")
            else:
                #If user not login redirect login
                return render(request, "network/login.html")

        #Add all post is_like (true if user do like)
        for post in all_posts:
            post.is_liked = post.user_like(request.user.id)

        paginator = Paginator(all_posts, 10) # Show 10 post per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {"page_obj": page_obj, "form":form})
    

@login_required(login_url ="/login")
def profile(request, user_id):
    try:
        all_user_posts = Post.objects.filter(user=user_id).order_by('-created_at')
        user = User.objects.get(id=user_id)

        #Check if login user is followed ser
        is_follow = True
        try:
            follow = Follower.objects.get(user=request.user, followed_user=user)
        except Follower.DoesNotExist:
            is_follow = False   

        #add all post number of like
        for post in all_user_posts:
            post.is_liked = post.user_like(request.user.id)

        paginator = Paginator(all_user_posts, 10) # Show 10 post per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {"page_obj": page_obj, "is_follow": is_follow})
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

@login_required(login_url ="/login")
def following(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        #Get all follower and get post of the follower
        following_users_posts = Post.objects.none()
        followers = Follower.objects.filter(user=user)
        for f in followers:
            posts = Post.objects.filter(user=f.followed_user)
            if posts:
                following_users_posts = following_users_posts.union(posts)

        following_users_posts = following_users_posts.order_by('-created_at')
        
        #Add to all posts extra field
        for post in following_users_posts:
            post.is_liked = post.user_like(user_id)
            post.user_id = post.user.id
            post.username = post.user.username
            post.number_like = post.number_of_like

        # Convert objets Post to dictionary beacause like and dislike not want work in template
        posts_dict = [post.__dict__ for post in following_users_posts]

        paginator = Paginator(posts_dict, 10) # Show 10 post per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/following.html", {"page_obj": page_obj})
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        # Query for requested post
        post = Post.objects.get(user=request.user, id=post_id)

        # Return post contents
        if request.method == "GET":
            return JsonResponse(post.serialize())

        # Update whether post is content
        elif request.method == "PUT":
            if request.user.id == post.user.id:
                data = json.loads(request.body)
                if data.get("content") is not None:
                    post.content = data["content"]
                post.save()
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                "error": "Only user post can edit this post."
            }, status=400)

        # Post must be via GET or PUT
        else:
            return JsonResponse({
                "error": "GET or PUT request required."
            }, status=400)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)


@csrf_exempt
@login_required
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    user = request.user

    # Get if user did like to post
    if request.method == "GET":
        try:
            like = Like.objects.get(user=user, post=post_id)
        except Like.DoesNotExist:
            return JsonResponse({"error": "Like not found."}, status=404)
        return JsonResponse(like.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        #If like exist, delete ralation usr post
        try:
            like = Like.objects.get(user=user, post=post_id)
            like.delete()
            number_like = post.number_of_like()
            return JsonResponse({"like":False,"number_like":number_like})
        except Like.DoesNotExist:
            #If like not exit then I create relation post user
            post = Post.objects.get(id=post_id)

            Like.objects.create(user=user, post=post)
            post = Post.objects.get(id=post_id)
            number_like = post.number_of_like()
            return JsonResponse({"like":True,"number_like":number_like})

    # Like must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def toggle_follow(request, user_id):
    followed_user = User.objects.get(id=user_id)
    user = request.user
    
    if request.method == "GET":
        try:
            follow = Follower.objects.get(user=user, post=post_id)
        except Follower.DoesNotExist:
            return JsonResponse({"error": "Follower not found."}, status=404)
        return JsonResponse(post_like.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        try:
            follow_instance = Follower.objects.get(user=user, followed_user=followed_user)
            # If user follow, unfollow
            follow_instance.delete()


            number_follower = followed_user.number_of_followers()
            return JsonResponse({"follow": False,"number_follower": number_follower})
        except Follower.DoesNotExist:
            # If unfollow, follow
            Follower.objects.create(user=user, followed_user=followed_user)
            number_follower = followed_user.number_of_followers()
            return JsonResponse({"follow": True,"number_follower":number_follower})

    # Like must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

def error(request):
    return render(request, 'auctions/error.html')