from __future__ import annotations
from lk import models

NOT_IMPLEMENT_ERROR = NotImplementedError('Code block is not implemented yet')


def get_name(human_id: int) -> models.Human:
    query = models.Human.objects.filter(human_id=human_id)

    if not len(query):
        raise KeyError("Invalid route")

    return query[0]


def get_page(route: str) -> models.Page:
    query = models.Page.objects.filter(route=route)
    if not len(query):
        raise KeyError("Invalid route")
    return query[0]


def get_phrase(tag: str) -> str:
    phrase = models.Phrase.objects.filter(tag=tag)
    if not len(phrase):
        raise KeyError("Invalid tag")
    return phrase[0].phrase


def get_routes() -> list[str]:
    return [i.route for i in models.Page.objects.all()]


def pages() -> list[models.Page]:
    return [get_page(route) for route in get_routes()]
