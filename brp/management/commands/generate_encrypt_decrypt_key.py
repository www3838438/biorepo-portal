from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        key = Fernet.generate_key()
        print(key)
        key = Fernet(key)
