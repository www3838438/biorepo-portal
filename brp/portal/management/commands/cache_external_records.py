# encoding: utf-8
import datetime

from portal.ehb_service_client import ServiceClient
from portal.models.protocols import Protocol, Organization, DataSource

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import get_cache

from portal.ehb_service_client import ServiceClient

cache = get_cache('redis')


class Command(BaseCommand):

    def cache_records(self):
	datasources = DataSource.objects.all()
	er_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD)
	for ds in datasources:
	    ers = er_rh.query({'external_system_id': ds.ehb_service_es_id})[0]['external_record']
	    for record in ers:
		cache.set('externalrecord_{0}'.format(record.id), record.json_from_identity(record))
	print 'Caching of ExternalRecords complete'

    def handle(self, *args, **options):
	self.cache_records()
