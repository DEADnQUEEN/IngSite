import datetime
import decimal

import django.db.models
from django import template
from typing import Final
from .. import models

register = template.Library()
SEP: Final = "_sep_"


@register.filter
def get_dict_values(value: dict):
    return value.values()


@register.filter
def get_dict_items(value: dict):
    return value.items()


@register.filter
def get_description(value: str, capitalize: bool = False):
    text = " ".join(
        [
            models.States.objects.filter(name=t)[0].description
            if len(models.States.objects.filter(name=t)) == 1
            else value
            for t in value.split(' ')
        ]
    )
    return text.capitalize() if capitalize else text


@register.filter
def concat(value, unite_to):
    return str(value) + str(unite_to)


@register.filter
def value_by_index(values: iter, index: int):
    return values[index]


@register.filter
def replace_to_dots(value: str, replace):
    return value.replace(replace, '.')


@register.filter
def replace_sep(value: str, replace):
    return value.replace(SEP, replace)


@register.filter
def count_finances(value: list[models.Finance]):
    s: decimal.Decimal = decimal.Decimal('0.0')
    for i in range(len(value)):
        s += value[i].amount
    return round(s, 2)


@register.filter
def count_coins(value: list[models.Coins]):
    s: decimal.Decimal = decimal.Decimal('0.0')
    if len(value) == 0:
        return s
    last_date: datetime.date = value[0].data
    i = 0
    while i < len(value):
        s *= 1.12
        while value[i].data.month == last_date.month and i < len(value):
            s += value[i].amount
            i += 1
    return round(s, 2)


@register.filter
def as_list(value: iter):
    return list(value)


@register.filter
def as_str(value):
    if isinstance(value, datetime.time):
        return value.strftime('%H:%M')
    if isinstance(value, datetime.date):
        return value.strftime('%Y-%m-%d')
    return str(value)


@register.filter
def as_str_date(value: datetime.date):
    return value.strftime('%d %B %Y')


@register.filter
def get_verbose_name(model: django.db.models.Model):
    return model._meta.verbose_name


@register.filter
def get_model_name(model: django.db.models.Model):
    return model._meta.model_name


@register.filter
def get_value_from_dict(dictionary: dict, key):
    return dictionary[key]
