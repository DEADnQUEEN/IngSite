from django.urls import path
from django.shortcuts import redirect
import inspect
from . import views

urlpatterns = [
    path(i[0] + '/', i[1]) for i in inspect.getmembers(views, inspect.isfunction)
]

urlpatterns.append(path("", lambda x: redirect('lk/')))
