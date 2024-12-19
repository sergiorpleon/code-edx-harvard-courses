from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
#from django.model import DoesNotExist
from .models import User, Listing, Bid, Watchlist, Comment, Category


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'category', 'image']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        widgets = {
            'bid_amount': forms.TextInput(attrs={"placeholder": "Bid"})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5})
        }

def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"active_listings": active_listings})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url ="/login")
def create_listing(request):
    """Before create listig with form input value add user to form instance"""
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.seller = request.user
            form.instance.current_bid = form.cleaned_data["starting_bid"]
            form.save()

            #return HttpResponseRedirect(reverse("index"))
            form = ListingForm()
            return render(request, 'auctions/create_listing.html', {'form': form, 'create_message':'Listing craeted successfull'})
        else:
            form = ListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form})

def listing(request, id):
    try:
        """Get all objects requires for template"""
        listing = Listing.objects.get(id=id)
        comments = Comment.objects.filter(listing=id).order_by('comment_time')
        bidform = BidForm()
        commentform = CommentForm()
        list_bid = Bid.objects.filter(listing=listing).order_by('-bid_time')

        """Build var active_whatchlist. First get user whatchlist."""
        active_whatchlist = False
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            user_watchlist = Watchlist.objects.filter(user=user).first()

            """Secod check that user ave instance of whatchlist and check that listings of whatchlist containt the current listing"""
            if user_watchlist:
                if user_watchlist.listings.filter(id=id).count() > 0:
                    active_whatchlist = True

            return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments, 'list_bid':list_bid, 'active_whatchlist': active_whatchlist, 'bidform': bidform, 'commentform': commentform})
        return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'list_bid':list_bid, 'active_whatchlist': active_whatchlist, 'bidform': bidform, 'commentform': commentform})
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))


@login_required(login_url ="/login")
def add_whatchlist(request, id):
    try:
        if request.user.is_authenticated:
            """Get user whatchlist and check if listings of watchlistig containt the listing."""
            active_whatchlist = False
            user = User.objects.get(id=request.user.id)
            user_watchlist = Watchlist.objects.get(user=user)
            if user_watchlist.listings.filter(id=id).count() > 0:
                active_whatchlist = True

            """If lising is in watchlist remove listing of watchlist. If lising is not in watchlist add listing to watchlist."""
            watchlist, created = Watchlist.objects.get_or_create(user=user)
            listing = Listing.objects.get(id=id)
            if active_whatchlist:
                watchlist.listings.remove(listing)            
            else:
                watchlist.listings.add(listing)

            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            return HttpResponseRedirect(reverse("listing", args=[id]))
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

@login_required(login_url ="/login")
def add_bid(request, id):
    try:
        """Get all objects requires for template"""
        listing = Listing.objects.get(id=id)
        comments = Comment.objects.filter(listing=id).order_by('comment_time')
        bidform = BidForm()
        commentform = CommentForm()

        if request.user.is_authenticated:
            #bid1 = Bid.objects.filter(bidder=request.user.id, listing=listing.id).first()
            #bidform = BidForm(bid1)

            if request.method == 'POST':
                bidform = BidForm(request.POST)
                if bidform.is_valid():
                    """Check that new bid bigger that current bid"""
                    if listing.current_bid < bidform.cleaned_data["bid_amount"]:

                        """Update field current_bid with new form value"""
                        listing.current_bid = bidform.cleaned_data["bid_amount"]
                        listing.save()
                        
                        """Craete new bid"""
                        Bid.objects.create(bidder=request.user, listing=listing, bid_amount=bidform.cleaned_data["bid_amount"])
                    else:
                        error_message = "New value of bid less than current"
                        return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'bidform': bidform, 'commentform': commentform, 'error_message': error_message})

            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            return HttpResponseRedirect(reverse("listing", args=[id]))
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

@login_required(login_url ="/login")
def add_comment(request, id):
    try:
        #bidform = BidForm()
        #comments = Comment.objects.filter(listing=id).order_by('comment_time')

        """Get listing that match with id and create comment related with listing with form value"""
        listing = Listing.objects.get(id=id)
        commentform = CommentForm()
        if request.user.is_authenticated:
            if request.method == 'POST':
                commentform = CommentForm(request.POST)
                if commentform.is_valid():
                    Comment.objects.create(commenter=request.user, listing=listing, content=commentform.cleaned_data["content"])

            #return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'bidform': bidform, 'commentform': commentform})
            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            #return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'bidform': bidform, 'commentform': commentform})
            return HttpResponseRedirect(reverse("listing", args=[id]))
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))
        
@login_required(login_url ="/login")
def close_listing(request, id):
    try:
        #comments = Comment.objects.filter(listing=id).order_by('comment_time')
        #bidform = BidForm()
        #commentform = CommentForm()

        if request.user.is_authenticated:
            """Get listing that match with id and change property is_active to False"""
            listing = Listing.objects.get(id=id)
            listing.is_active=False
            listing.save()

            #return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'bidform': bidform, 'commentform': commentform})
            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            listing = Listing.objects.get(id=id)
            #return render(request, 'auctions/listing.html', {'listing': listing, 'comments':comments,'bidform': bidform, 'commentform': commentform})
            return HttpResponseRedirect(reverse("listing", args=[id]))

    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

@login_required(login_url ="/login")
def watchlist(request):
    
    if request.user.is_authenticated:
        """Get whatchlist of user"""
        user = User.objects.get(id=request.user.id)
        #watchlistselect = Watchlist.objects.get(user=user)
        watchlistselect = Watchlist.objects.filter(user=user).first()

        """Get listings of user whatchlist and render"""
        user_watchlist=[]
        if watchlistselect:
            user_watchlist = watchlistselect.listings.all()
        
        return render(request, 'auctions/watchlist.html', {'user_watchlist': user_watchlist})

    return HttpResponseRedirect(reverse("index"))


def categories(request):
    try:
        """Get all category and render"""
        list_categories = Category.objects.all()
        return render(request, 'auctions/categories.html', {'list_categories': list_categories})
    except Category.DoesNotExist:
        return HttpResponseRedirect(reverse("error"))

def listings_category(request, id):
    """Empty category"""
    if id==0:
        """Case category empty redender listings_category.html with listings with out category"""
        listings = Listing.objects.filter(category=None, is_active=True)
        return render(request, 'auctions/listings_category.html', {'listings': listings, 'category': None})
    else:
        try:
            """Case category exist redender listings_category.html with category and listings of category"""
            category = Category.objects.get(id=id)
            listings = Listing.objects.filter(category=category, is_active=True)
        
            return render(request, 'auctions/listings_category.html', {'listings': listings, 'category': category})
        except Category.DoesNotExist:
            return HttpResponseRedirect(reverse("error"))

def error(request):
    return render(request, 'auctions/error.html')
