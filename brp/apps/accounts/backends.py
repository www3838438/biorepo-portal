from django.db import transaction
from registration.models import RegistrationProfile
from registration.backends.default import Backend

from accounts.models import UserProfile
from accounts.forms import ChopRegistrationForm


class DefaultBackend(Backend):
    @transaction.commit_on_success
    def register(self, request, form):
        cleaned_data = form.cleaned_data

        user = form.save(commit=False)
        # new user registration requires review, so we set the user to inactive
        # by default
        user.is_active = False
        user.save()

        # create user profile
        profile = UserProfile(user=user, reason=cleaned_data['reason'],
                              eula=cleaned_data['eula'],
                              institution=cleaned_data['institution'])
        profile.save()

        # create the registration profile
        registration_profile = RegistrationProfile.objects.create_profile(user)

        # provide the ``moderated`` to the user registration email to
        # determine whether the activation or verification link should
        # be sent in the email
        self._send_registration_email(request, registration_profile)
        return user

    def get_registration_form_class(self, request):
        return ChopRegistrationForm
