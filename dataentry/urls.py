from django.conf.urls import url
from .views import pds_dataentry_list, pds_dataentry_create, pds_dataentry_form, \
    pds_dataentry_start
urlpatterns = [
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/list/$',
        pds_dataentry_list),
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/create/$',
        pds_dataentry_create),
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/record/(?P<record_id>\d+)/start/$',
        pds_dataentry_start),
    url(
        r'^protocoldatasource/(?P<pds_id>\d+)/subject/(?P<subject_id>\d+)/record/(?P<record_id>\d+)/form_spec/(?P<form_spec>[a-z0-9-_]+)/$',  # noqa
        pds_dataentry_form),
]
