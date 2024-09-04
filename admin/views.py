from __future__ import annotations
from typing import Final
from django.shortcuts import render
import django.http.request
import django.http.response
import inspect
from lk import models
from lk.base_models import Page
import os
from django.db.models import Field
from django.db import connections


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

    fields: list[Field] = render_object['model']._meta.fields
    render_object['fields'] = {
        fields[i]: fields[i].db_type(connections['default'])
        if fields[i].db_type(connections['default']) not in ["integer", 'float']
        else "number"
        for i in range(len(fields))
    }

    if request.method == 'POST':
        data = {
            fields[i].name: fields[i].to_python(request.POST[fields[i].name])
            for i in range(len(fields))
            if len(request.POST[fields[i].name]) > 0
        }

        if len(data.keys()) == 0:
            FILTER_OBJECTS[model_name].objects.all()

        render_object['models'] = FILTER_OBJECTS[model_name].objects.filter(**data)

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )
