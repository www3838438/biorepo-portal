
from django.core.management.base import BaseCommand
from django.core.cache import cache

from api.ehb_service_client import ServiceClient


# from rest_framework.response import Response


class Command(BaseCommand):
    def handle(self, *args, **options):
        erl_rh = ServiceClient.get_rh_for(record_type=ServiceClient.EXTERNAL_RECORD_LABEL)
        labels = erl_rh.query()
        cache.set('ehb_labels', labels)
        if hasattr(cache, 'persist'):
            cache.persist('ehb_labels')

        print("caching of ehb_labels complete")
