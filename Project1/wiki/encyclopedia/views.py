from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.contrib import messages
import random
from . import *
from . import util
from markdown2 import Markdown

class SearchBar(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search Encyclopedia"
    }))

class CreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Page Title"
    }))
    text = forms.CharField(label="",widget=forms.Textarea(attrs={
        "placeholder": "Enter page content (Use Github Markdown)",
    }))

class EditForm(forms.Form):
    text = forms.CharField(label="",widget=forms.Textarea(attrs={
        "placeholder": "Enter page content (Use Github Markdown)",
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

def create(request):

    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "create_form": CreateForm(),
            "search_form": SearchBar()
        })
    
    elif request.method == "POST":
        form = CreateForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]

        else:
            messages.error(request, "Form not valid, try again.")
            return render(request, "encyclopedia/create.html", {
                    "create_form": form,
                    "search_form": SearchBar()
                })
        
        if util.get_entry(title):
            messages.error(request, "Title alredy exists, try again.")
            return render(request, "encyclopedia/create.html", {
                    "create_form": form,
                    "search_form": SearchBar()
                })
        
        util.save_entry(title, text)
        messages.success(request, (f"New page {title} was created with success.", request))
        return redirect(reverse('entry', args=[title]))

def edit(request, title):
    if request.method == "GET":
        text = util.get_entry(title)
    
        if text == None:
            messages.error("The page you are trying to edit doesn't exist, try to create a new page instead.")

        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": EditForm(initial={'text':text}),
                "search_form": SearchBar()
            })
        
    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            messages.success(request, f"Entry {title} was edited succesfully")
            return redirect(reverse('entry', args=[title]))
        
        else:
            messages.error(request, f"The edit was not valid, try again!")
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": form,
                "search_form": SearchBar()
            })
        
def random_page(request):
    titles = util.list_entries()
    title = random.choice(titles)
    return redirect(reverse('entry', args=[title]))


        

        
        
        

