from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views.protocol import New_protocol_usr


urlpatterns = [
    url(
        r'^new_protocol_usr/$',
        login_required(New_protocol_usr.as_view())),
]
