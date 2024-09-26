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

FILTER_OBJECTS['User'] = models.User

FILTER_OBJECTS_HIDE: Final[dict[str: tuple]] = {
    key: ()
    for key in FILTER_OBJECTS.keys()
}

FILTER_OBJECTS_HIDE['User'] = ('password', 'last_login', 'is_superuser')


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


def add(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if request.method != "POST" or not request.user.is_superuser:
        return django.shortcuts.redirect('../lk/')

    json_data: dict = json.loads(request.body)

    model: models.models.Model = FILTER_OBJECTS[json_data['table']]

    data = {}

    for k in json_data['model-content'].keys():
        field: models.models.Field = model._meta.get_field(k)
        if isinstance(field, models.models.ForeignKey):
            f: models.models.ForeignKey = field
            data[k] = FILTER_OBJECTS[
                f.remote_field.model.__name__
            ].objects.filter(id=json_data['model-content'][k]).first()
        else:
            data[k] = json_data['model-content'][k]

    FILTER_OBJECTS[json_data['table']].objects.create(**data)

    return django.http.response.HttpResponse("")


def save(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if request.method != "POST" or not request.user.is_superuser:
        return django.shortcuts.redirect('../lk/')
    json_data: dict = json.loads(request.body)

    model_object: models.models.Model = FILTER_OBJECTS[
        json_data['table']
    ].objects.filter(id=json_data['model-content']['id'])[0]

    keys = list(json_data['model-content'].keys())
    for i in range(2, len(keys)):
        setattr(model_object, keys[i], json_data['model-content'][keys[i]])

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
    render_object['fields'] = {}
    for i in range(len(fields)):
        if fields[i].name in FILTER_OBJECTS_HIDE[model_name]:
            continue
        if fields[i].db_type(connections['default']) not in ["integer", 'float']:
            render_object['fields'][fields[i]] = fields[i].db_type(connections['default'])
        else:
            render_object['fields'][fields[i]] = "number"

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )
