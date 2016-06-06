from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from accounts import models


def create_user_profiles(sender, **kwargs):
    users = User.objects.filter(profile__isnull=True)
    for user in users:
        profile = models.UserProfile(user=user)
        if user.email.endswith('@email.chop.edu'):
            profile.institution = "The Children's Hospital of Philadelphia"
        profile.save()

post_migrate.connect(create_user_profiles, sender=models)
