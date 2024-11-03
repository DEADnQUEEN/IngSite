from __future__ import annotations
import json
from typing import Final
from django.shortcuts import render
import django.http.request
import django.http.response
from lk import models
from .models import Page
import os
from django.db.models import Field
from django.db import connections


def common_options(field: django.db.models.Field) -> dict:
    f_type = field.db_type(connections['default'])
    return {
        "name": field.verbose_name,
        "type": f_type if f_type not in ['integer', 'float'] else "number",
        "values": [
            field.value_from_object(model)
            for model in field.model.objects.all()
        ]
    }


def input_options(field: django.db.models.Field) -> dict[str, any]:
    return {
        'template': "Base/input.html",
        'options': common_options(field),
    }


def id_options(field: django.db.models.AutoField) -> dict[str, any]:
    return {
        "template": "Base/cmb_id.html",
        "options": common_options(field),
        "objects": {
            obj.id: obj.id
            for obj in field.model.objects.all()
        }
    }


def foreign_key_options(field: django.db.models.ForeignKey) -> dict[str, any]:
    return {
        "template": "Base/combobox.html",
        "options": common_options(field),
        "objects": {
            obj.id: obj.__str__()
            for obj in field.related_model.objects.all()
        }
    }


# model_name: (model_class, (name_of_hidden_fields))
FILTER_OBJECTS: Final[dict[str: tuple[django.db.models.Model, list[str]]]] = {
    model.__name__: (
        model, [
            field.name for field in model._meta.fields
        ]
    )
    for model in [
        models.User, models.Student, models.Visits, models.Courses, models.Finance, models.Human, models.Connect
    ]
}

for remove_item in ['password', 'is_superuser', 'last_login']:
    FILTER_OBJECTS['User'][1].remove(remove_item)

TODO: dict[any, callable] = {
    models.models.AutoField: id_options,
    models.models.ForeignKey: foreign_key_options
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

    for k in json_data['model-content'].keys():
        field: models.models.Field = model_object._meta.get_field(k)

        if isinstance(field, models.models.ForeignKey):
            f: models.models.ForeignKey = field
            attr = FILTER_OBJECTS[
                f.remote_field.model.__name__
            ].objects.filter(id=json_data['model-content'][k]).first()
        else:
            attr = json_data['model-content'][k]
        setattr(model_object, k, attr)

    model_object.save()

    return django.http.response.HttpResponse("")


def filter_page(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    model: django.db.models.Model = FILTER_OBJECTS[os.path.split(request.path)[-1]][0]
    render_object: dict[str, any] = {
        'title': model.__name__,
        "model": model,
        "content": {}
    }

    field_order: tuple[dict, dict[str, any]] = (
        {}, {}
    )
    actions = (
        lambda f: TODO[type(field)](f),
        lambda f: input_options(f),
    )

    field_names = FILTER_OBJECTS[model.__name__][1]

    for i in range(len(field_names)):
        field = model._meta.get_field(field_names[i])
        is_order = type(field) not in TODO.keys()
        field_order[is_order][field] = actions[is_order](field)

    for order in field_order:
        for key in order.keys():
            render_object['content'][key] = order[key]

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )
