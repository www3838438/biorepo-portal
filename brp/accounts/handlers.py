from accounts.models import UserProfile


def reset_eula(sender, instance, created, **kwargs):
    '''
    Resets all user's EULA agreement when it changes.
    '''
    if instance.url.lower() == '/eula/':
        UserProfile.objects.update(eula=False)
