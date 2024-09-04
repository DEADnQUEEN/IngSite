from django.urls import include, path, re_path
from django.views.static import serve
from . import settings


urlpatterns = [
    path('', include('lk.urls')),
    path('admin/', include('admin.urls')),
#    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
