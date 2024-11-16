from __future__ import annotations
import django.http.request
import django.http.response
import django.shortcuts
from .forms import UserLogin
import django.contrib.auth
import django.db.models.fields.related
from .models import User, Connect
from admin.models import Page
import hashlib
from django.contrib import messages


def login(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    if request.method == 'GET':
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": UserLogin()
            }
        )

    form = UserLogin(request.POST)

    if not form.is_valid():
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "content": {
                    'inputs': form
                }
            }
        )

    user: User = User.objects.filter(login=form.data['login']).first()

    if user is None:
        messages.error(request, 'Телефон введен неверно либо не зарегистрирован')
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": form
            }
        )

    if user.password != hashlib.sha3_256(str(form.data['password']).encode('UTF-8')).hexdigest():
        messages.error(request, 'Пароль неверный')
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": form
            }
        )

    django.contrib.auth.login(request, user)
    return django.shortcuts.redirect('/lk')


def lk(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if not request.user.is_authenticated:
        messages.error(request, 'Пройдите авторизацию')
        return django.shortcuts.redirect("/login")

    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    connects: list[Connect] = Connect.objects.filter(user_id=request.user.id)

    query = {}

    for i in range(len(connects)):
        if connects[i].student.human_id not in list(query.keys()):
            query[connects[i].student.human_id] = []

        query[connects[i].student.human_id].append(connects[i].student)

    return django.shortcuts.render(request, page.template, {"title": page.title, "query": query})


def logout(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    django.contrib.auth.logout(request)
    return django.shortcuts.redirect("/login")
