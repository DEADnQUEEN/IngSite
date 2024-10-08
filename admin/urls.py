from django.urls import path
from . import views

urlpatterns = [
    path("", views.main),
    path("save", views.save),
    path("add", views.add)
]

model_list = [*views.FILTER_OBJECTS.keys()]
for i in range(len(model_list)):
    urlpatterns.append(path(f"{model_list[i]}", views.filter_page))
