from django import forms
from django.shortcuts import render
from markdown2 import markdown
from django.shortcuts import render, redirect
from . import util
from random import randint


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()

    })


def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/404.html", {'content': content, 'title': title})
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})


def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})


def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/create.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/create.html", {"message": "This page already exists.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/create.html")


def search(request):
    q = request.GET.get('q')
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {'entries': util.list_entries(), 'q': q})


def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries) - 1)]
    return redirect("entry", title=random_title)
