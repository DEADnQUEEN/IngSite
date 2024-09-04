from __future__ import annotations
from typing import Final
from django.shortcuts import render
import django.http.request
import django.http.response
import inspect
from lk import models
from lk.base_models import Page
import os


FILTER_OBJECTS: Final = {
    member[0]: member[1]
    for member in inspect.getmembers(models, inspect.isclass)
    if models.models.Model in member[1].__bases__
}


def main(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if not request.user.is_superuser:
        return django.shortcuts.redirect('/lk')

    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    return django.shortcuts.render(
        request,
        page.template,
        {
            "title": page.title,
        }
    )


def filter_page(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    model_name = os.path.split(request.path)[-1]
    render_object = {
        'title': model_name,
        "model": FILTER_OBJECTS[model_name],
        "models": FILTER_OBJECTS[model_name].objects.all()
    }

    if request.method == 'POST':
        data = {
            field.name: request.POST[field.name]
            if "id" not in field.name
            else int(str(request.POST[field.name]))
            for field in FILTER_OBJECTS[model_name]._meta.fields
            if len(request.POST[field.name]) > 0
        }
        render_object['models'] = FILTER_OBJECTS[model_name].objects.filter(**data)

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )
