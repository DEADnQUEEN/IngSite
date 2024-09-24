from __future__ import annotations
import json
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


FILTER_OBJECTS: Final[dict[str: django.db.models.Model]] = {
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


def save(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if request.method != "POST" or not request.user.is_superuser:
        return django.shortcuts.redirect('../lk/')
    json_data: dict = json.loads(request.body)

    model_object: models.models.Model = FILTER_OBJECTS[json_data['table']].objects.filter(id=json_data['id'])[0]

    keys = list(json_data.keys())
    for i in range(2, len(keys)):
        setattr(model_object, keys[i], json_data[keys[i]])

    model_object.save()

    return django.http.response.HttpResponse("")


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

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )
