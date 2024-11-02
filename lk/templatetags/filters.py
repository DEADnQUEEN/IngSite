import decimal
from django import template
from typing import Final
from .. import models
from .. import forms

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
def as_list(value: iter):
    return list(value)


@register.filter
def as_str(value):
    return str(value)


@register.filter
def is_register(value):
    return type(value) is forms.UserRegister


@register.filter
def get_value_from_dict(dictionary: dict, key):
    return dictionary[key]
