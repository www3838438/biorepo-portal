from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views.protocol import New_protocol_usr, Fn_in_progress
from .views.brp_commands import CacheSubjects


urlpatterns = [
    url(
        r'^new_protocol_usr/$',
        login_required(New_protocol_usr.as_view()),
        name='new_protocol_usr'),
    url(
        r'^fn_in_progress/$',
        login_required(Fn_in_progress.as_view())),
    url(
        r'^cache_subjects/$',
        login_required(CacheSubjects.as_view()),
        name='cache_subjects'),
]
