from __future__ import annotations
import json
from typing import Final
from django.shortcuts import render
import django.http.request
import django.http.response
from lk import models
from .models import Page
from django.db.models import Field
from django.db import connections
from django.forms.models import model_to_dict
from .forms import model_forms


def common_options(field: django.db.models.Field) -> dict:
    f_type = field.db_type(connections['default'])
    return {
        'field_name': field.name,
        "name": field.verbose_name,
        "type": f_type if f_type not in ['integer', 'float'] else "number",
    }


def input_options(field: django.db.models.Field) -> dict[str, any]:
    return {
        'template': "Base/input.html",
        'options': common_options(field),
    }


def id_options(field: django.db.models.AutoField) -> dict[str, any]:
    opt = {
        "template": "Base/combobox.html",
        "options": common_options(field)
    }
    opt["options"]["objects"] = {
        obj.id: obj.id
        for obj in field.model.objects.all()
    }
    return opt


def foreign_key_options(field: django.db.models.ForeignKey) -> dict[str, any]:
    opt = {
        "template": "Base/combobox.html",
        "options": common_options(field)
    }
    opt["options"]["objects"] = {
        obj.id: str(obj)
        for obj in field.related_model.objects.all()
    }
    return opt


# model_name: (model_class, (name_of_hidden_fields))
FILTER_OBJECTS: Final[dict[str: tuple[django.db.models.Model, list[str]]]] = {
    model.__name__: (
        model, [
            field.name for field in model._meta.fields
        ]
    )
    for model in [
        models.User, models.Student, models.Visits,
        models.Courses, models.Finance, models.Human,
        models.Connect, models.Coins, models.States
    ]
}

for remove_item in ['password', 'is_superuser', 'last_login']:
    FILTER_OBJECTS['User'][1].remove(remove_item)

TODO: dict[any, callable] = {
    models.models.AutoField: id_options,
    models.models.ForeignKey: foreign_key_options
}


def get_model_fields(model: type(django.db.models.Model)):
    field_names = FILTER_OBJECTS[model._meta.model_name.capitalize()][1]
    fields = {}

    for i in range(len(field_names)):
        field: Field = model._meta.get_field(field_names[i])
        tp = type(field)
        func = input_options
        if tp in TODO.keys():
            func = TODO[tp]
        fields[field.name] = func(field)

    return fields


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


def add(request: django.http.request.HttpRequest, model_name: str) -> django.http.response.HttpResponse:
    if not request.user.is_superuser:
        return django.shortcuts.redirect('../lk/')

    model_name = model_name.capitalize()
    if model_name not in FILTER_OBJECTS.keys():
        return django.shortcuts.redirect('/admin/')

    model: models.models.Model = FILTER_OBJECTS[model_name][0]
    if request.method == "GET":
        return django.shortcuts.render(
            request,
            "Page/add_model.html",
            {
                'title': model._meta.verbose_name,
                "fields": get_model_fields(model),
            }
        )

    form = model_forms[model_name](request.POST)

    if not form.is_valid():
        return django.shortcuts.render(
            request,
            "Page/admin forms.html",
            {
                'title': model_name,
                "form": form
            }
        )

    model_obj = form.save(True)

    return django.http.response.HttpResponse("")


def save(request: django.http.request.HttpRequest, model_name) -> django.http.response.HttpResponse:
    if request.method != "POST" or not request.user.is_superuser:
        return django.shortcuts.redirect('../lk/')

    model_name = model_name.capitalize()
    if model_name not in FILTER_OBJECTS.keys():
        return django.shortcuts.redirect('/admin/')

    if model_name not in FILTER_OBJECTS.keys():
        return django.shortcuts.redirect('/admin/')

    json_data: dict = json.loads(request.body)

    j_keys: list = [*json_data.keys()]
    model_object: models.models.Model = FILTER_OBJECTS[model_name][0].objects.filter(id=json_data['id'])[0]

    for key in range(1, len(j_keys)):
        setattr(model_object, j_keys[key], json_data[j_keys[key]])

    model_object.save()

    return django.http.response.HttpResponse("Saved!")


def filter_page(request: django.http.request.HttpRequest, model_name: str) -> django.http.response.HttpResponse:
    model_name = model_name.capitalize()

    if model_name not in FILTER_OBJECTS.keys():
        return django.shortcuts.redirect('/admin/')

    model: django.db.models.Model = FILTER_OBJECTS[model_name][0]

    field_names = FILTER_OBJECTS[model_name][1]

    render_object: dict[str, any] = {
        'title': model._meta.verbose_name,
        "model": model,
        "fields": get_model_fields(model),
        "values": (model_to_dict(m, fields=field_names) for m in model.objects.all())
    }

    return django.shortcuts.render(
        request,
        'Page/admin.html',
        render_object
    )


def show(request: django.http.request.HttpRequest, model_name) -> django.http.response.HttpResponse:
    return django.http.HttpResponse(model_forms[model_name]())
