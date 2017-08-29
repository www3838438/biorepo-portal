from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views.protocol import New_protocol_usr, Fn_in_progress


urlpatterns = [
    url(
        r'^new_protocol_usr/$',
        login_required(New_protocol_usr.as_view())),
    url(
        r'^fn_in_progress/$',
        login_required(Fn_in_progress.as_view())),
]
