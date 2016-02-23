# encoding: utf-8
import datetime
import json

from portal.ehb_service_client import ServiceClient
from portal.models.protocols import Protocol, Organization, DataSource

from django.db import models
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import get_cache

from portal.ehb_service_client import ServiceClient

cache = get_cache('default')


class Command(BaseCommand):

    def cache_records(self):
        datasources = DataSource.objects.all()
        protocols = Protocol.objects.all()
        for protocol in protocols:
            subs = protocol.getSubjects()
            if subs:
                subs_dict = [json.loads(subject.json_from_identity(subject)) for subject in subs]
                sk = '{0}_subjects'.format(protocol.id)
                cache.set(sk, json.dumps(subs_dict))
                # Make sure key lasts a day
                cache.expire(sk, 60*60*24)

        print 'Subject caching complete'

    def handle(self, *args, **options):
        self.cache_records()
