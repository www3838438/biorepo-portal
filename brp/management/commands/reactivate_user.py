import re

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs=1, type=int)

    def handle(self, *args, **options):
        user_id = options['user_id'][0]
        try:
            user = User.objects.get(pk=user_id)
        except user.DoesNotExist:
            raise CommandError('User with ID "%s" does not exist' % user_id)

        # cache_keys = cache.keys('*')
        for key in cache.keys('*'):
            if re.match('{0}.*login_attempts'.format(user.username), key):
                cache.delete(key)
                print('Login attempts deleted from cache')
        user.is_active = True
        user.save()
        print('User Reactivated')
