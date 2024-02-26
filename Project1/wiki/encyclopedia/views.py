from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from . import *
from . import util
from markdown2 import Markdown

class SearchBar(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchBar()
    })

def entry(request, title):
    
    entry_md = util.get_entry(title)

    if entry_md != None:
        entry_HTML = Markdown().convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_HTML,
            "search_form": SearchBar()
        })
    else:
        related_search = util.related_search(title)

        return render(request, "encyclopedia/error.html", {
            "title": title,
            "related_search": related_search,
            "search_form": SearchBar()
        })
    
def search(request):

    if request.method == "POST":
        form = SearchBar(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = util.get_entry(title)

            print("Search request: ", title)

            if entry_md:
                return redirect(reverse('entry', args=[title]))
            
            else:

                related_search = util.related_search(title)
                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "related_search": related_search,
                    "search_form": SearchBar()
                })
            
    redirect(reverse("index"))