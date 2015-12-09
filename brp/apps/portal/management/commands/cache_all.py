# encoding: utf-8
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def cache_all(self):
	call_command('cache_external_records')
	call_command('cache_subjects')

    def handle(self, *args, **options):
	self.cache_all()
