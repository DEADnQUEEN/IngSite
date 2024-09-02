from __future__ import annotations
from django.shortcuts import render
import django.http.request
import django.http.response
import func_tools


def main(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if not request.user.is_superuser:
        return django.shortcuts.redirect('/lk')

    page = func_tools.get_page(request.path_info)

    return django.shortcuts.render(
        request,
        page.template,
        {
            "title": page.title,
        }
    )





