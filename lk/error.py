import inspect

import django.http.request
import django.http.response
import django.core.exceptions
import django.shortcuts


def error(request: django.http.request.HttpRequest, ex):
    return django.shortcuts.render(request, 'Page/Error.html', {'test': type(ex)})
