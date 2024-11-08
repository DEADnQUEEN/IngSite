from __future__ import annotations
import django.http.request
import django.http.response
import django.shortcuts
from .forms import UserLogin, UserRegister
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

    user_login = User.objects.filter(login=form.data['login']).first()
    user_phone = User.objects.filter(phone=form.data['login']).first()
    user_mail = User.objects.filter(mail=form.data['login']).first()

    user: User = user_login if user_login is not None \
        else user_mail if user_mail is not None \
        else user_phone

    if user is None:
        messages.error(request, 'Логин, Телефон или Почта введены неверно')
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
