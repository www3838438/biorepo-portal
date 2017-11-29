import re

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        m_mode = cache.get('maintenance_mode')
        if m_mode:
            cache.delete('maintenance_mode')
            print('Maintenance Mode Off')
        else:
            cache.set('maintenance_mode', 1)
            cache.persist('maintenance_mode')
            print('Maintenance Mode On')
