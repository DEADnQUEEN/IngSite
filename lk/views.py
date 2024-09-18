from __future__ import annotations

import json

import django.http.request
import django.http.response
import django.shortcuts
from .forms import UserLogin, UserRegister
import django.contrib.auth
import django.db.models.fields.related
from .models import User, Connect
from .base_models import Page
import hashlib
from typing import Final


HELL: Final = {
    'integer': int,
    'text': str
}


def login(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    if request.method == 'GET':
        form = UserLogin()
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": form
            }
        )

    form = UserLogin(request.POST)

    if not form.is_valid():
        return django.shortcuts.render(request, page.template, {'title': page.title, "content": {'inputs': list(form)}})

    user_password_match = User.objects.filter(
        password=hashlib.sha3_256(str(form.data['password']).encode('UTF-8')).hexdigest()
    )

    user_login = user_password_match.filter(login=form.data['login']).first()
    user_phone = user_password_match.filter(phone=form.data['login']).first()
    user_mail = user_password_match.filter(mail=form.data['login']).first()

    user = user_login if user_login is not None \
        else user_mail if user_mail is not None \
        else user_phone

    if user is not None:
        django.contrib.auth.login(request, user)

    return django.shortcuts.redirect('/lk')


def register(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    if request.method == 'GET':
        form = UserRegister()
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": form
            }
        )

    form = UserRegister(request.POST)

    if not form.is_valid():
        return django.shortcuts.render(
            request,
            page.template,
            {
                'title': page.title,
                "form": form
            }
        )

    user = form.save(commit=True)

    django.contrib.auth.login(request, user)

    return django.shortcuts.redirect('/lk')


def lk(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    if not request.user.is_authenticated:
        return django.shortcuts.redirect("/register")

    page = Page.objects.filter(route=request.path).first()

    if page is None:
        raise Exception()

    connects = Connect.objects.filter(user_id=request.user.id)

    query = {}

    for i in range(len(connects)):
        if connects[i].student_id.human_id.id not in list(query.keys()):
            query[connects[i].student_id.human_id.id] = []

        query[connects[i].student_id.human_id.id].append(connects[i].student_id)

    return django.shortcuts.render(request, page.template, {"title": page.title, "query": query})


def logout(request: django.http.request.HttpRequest) -> django.http.response.HttpResponse:
    django.contrib.auth.logout(request)
    return django.shortcuts.redirect("/login")
