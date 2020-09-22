from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.create,name="create"),
    path("wiki/<str:title>",views.entry_page,name="entry"),
    path("random",views.random_page,name="random"),
    path('wiki/edit/<str:title>',views.editpage,name="edit"),
     path("search", views.search, name="search")
]
