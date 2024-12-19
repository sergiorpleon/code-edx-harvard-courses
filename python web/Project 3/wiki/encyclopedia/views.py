from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown
import random as random_function
from . import util

class CreateForm(forms.Form):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea())

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}))

def search(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            title = search_form.cleaned_data["search"]
            entry = util.get_entry(title)

            if entry is None:
                entries = util.list_entries()
                search_entries = []
                for element in entries:
                    if title in element:
                        search_entries.append(element)
                if len(search_entries):
                    return render(request, "encyclopedia/search.html", {
                        "search_form": search_form,
                        "entries": search_entries
                    })
    
                return render(request, "encyclopedia/search.html", {
                    "search_form": search_form,
                    "entries": []
                })
            
            else:
                return HttpResponseRedirect(reverse("entry", args=[title]))
                

    return render(request, "encyclopedia/search.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "search_form": SearchForm(),
            "message": f"Entry {title} not found"
        })
    else:
        markdower = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "search_form": SearchForm(),
            "title": title,
            "entry": markdower.convert(entry)
        })

def create(request):
    if request.method == "POST":
        entry_form = CreateForm(request.POST)
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]
            content = entry_form.cleaned_data["content"]
            
            entry = util.get_entry(title)
            if entry is None:
                util.save_entry(title, content)
                """" redirect to entry """
                return HttpResponseRedirect(reverse("entry", args=[title]))
    
            return render(request, "encyclopedia/create.html", {
                "search_form": SearchForm(),
                "entry_form": entry_form,
                "message": "Entry already exists"
            })
            
        else:
            return render(request, "encyclopedia/create.html", {
                "search_form": SearchForm(),
                "entry_form": entry_form,
                "message": "Form is not valid"
            })

    return render(request, "encyclopedia/create.html", {
            "search_form": SearchForm(),
            "entry_form": CreateForm(),
            "message": ""
        })


def edit(request, title):
    if request.method == "POST":
        entry_form = EditForm(request.POST)
        if entry_form.is_valid():
            content = entry_form.cleaned_data["content"]
            
            util.save_entry(title, content)
            """" redirect to entry """
            return HttpResponseRedirect(reverse("entry", args=[title]))
        

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "search_form": SearchForm(),
            "entry_form": entry_form,
            "message": "Form is not valid"
        })

    
    entry = util.get_entry(title)
    entry_form = EditForm({"content":entry})
    
    return render(request, "encyclopedia/edit.html", {
            "title": title,
            "search_form": SearchForm(),
            "entry_form": entry_form,
            "message": ""
        })

def random(request):
    entries = util.list_entries()
    title = random_function.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[title]))