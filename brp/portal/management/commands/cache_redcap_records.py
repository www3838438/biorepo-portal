# encoding: utf-8
import datetime

from portal.ehb_service_client import ServiceClient
from portal.models.protocols import Protocol, Organization, DataSource

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand
from redis import Redis

from portal.ehb_service_client import ServiceClient

cache = Redis(host='192.168.99.100')


class Command(BaseCommand):
    # TODO: Need service "accounts" on each protocol to facilitate access to these
    # redcap studies.
    def cache_records(self):
        datasources = DataSource.objects.all()
        er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
        for ds in datasources:
            ers = er_rh.query({'external_system_id': ds.ehb_service_es_id})[0]['external_record']
            for record in ers:
                print record.record_id

    def handle(self, *args, **options):
        self.cache_records()
