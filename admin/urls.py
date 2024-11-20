from django.urls import path
from . import views

urlpatterns = [
    path("", views.main),
    path("save/<str:model_name>", views.save),
    path("add/<str:model_name>", views.add),
    path("<str:model_name>", views.filter_page),
    path("show/<str:model_name>", views.show)
]
