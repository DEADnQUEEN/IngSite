import django.db.models
from django import template
from .. import models
from .filters import SEP
from admin.views import FILTER_OBJECTS

register = template.Library()


def get_from_db(model_id: int, model):
    item = model.objects.filter(id=model_id).first()
    if item is None:
        raise ValueError()
    return models.model_to_dict(item)


@register.filter
def column_value(model: django.db.models.Model, column: django.db.models.Field):
    return column.value_from_object(model)


@register.filter
def dict_key(dictionary: dict, key):
    if key not in dictionary.keys():
        raise KeyError(f"{key} is not exists")

    return dictionary[key]


@register.filter
def get_model_list(_):
    return [key for key in FILTER_OBJECTS.keys()]


@register.filter
def get_model_fields(model):
    return [key for key in models.model_to_dict(model).keys()]


@register.filter
def get_name(human_id: int):
    return get_from_db(human_id, models.Human)


@register.filter
def get_student(student_id: int):
    return get_from_db(student_id, models.Student)


@register.filter
def get_course(course_id: int):
    return get_from_db(course_id, models.Courses)


@register.filter
def get_name(human: models.Human):
    return " ".join([human.name.capitalize(), human.surname.capitalize(), human.father_name.capitalize()])


@register.filter
def get_tag(query, tag):
    return SEP.join(
        [
            models.model_to_dict(query[i])[tag]
            for i in range(len(query))
            if query[i] is not None
        ]
    )


@register.filter
def get_initials(value: models.Human):
    return " ".join([value.surname.capitalize(), value.name[0].upper() + ".", value.father_name[0].upper() + "."])


@register.filter
def get_all_visits(_):
    return models.States.objects.filter(id__range=(10, 99))


@register.filter
def get_all_states(_):
    return models.States.objects.filter(id__range=(1, 9))
