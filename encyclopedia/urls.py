from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<title>', views.entry, name="entry"),
    path("edit/<title>", views.edit, name="edit"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("random", views.random_page, name="random"),
]
