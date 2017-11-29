from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views.pds import StartView, CreateView, FormView
urlpatterns = [
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/create/$',
        login_required(CreateView.as_view())),
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/record/(?P<record_id>\d+)/start/$',
        login_required(StartView.as_view())),
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/record/(?P<record_id>\d+)/form_spec/(?P<form_spec>[a-z0-9-_]+)/$',  # noqa
        login_required(FormView.as_view())),
]
