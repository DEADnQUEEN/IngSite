from django.urls import path
import inspect
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path(i[0] + '/', i[1]) for i in inspect.getmembers(views, inspect.isfunction)
]

urlpatterns.append(path("", lambda x: redirect('main/')))
