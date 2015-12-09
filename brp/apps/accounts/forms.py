from django import forms
from django.contrib.auth import forms as auth_forms, authenticate
from django.utils.translation import ugettext_lazy as _
from registration.forms import EmailOnlyRegistrationForm
from registration.utils import validate_password, generate_random_username

MIN_PASSWORD_LENGTH = 8

pw_help_text = ('CHOP employees do not need to supply a password. For all '
                'other users, passwords must be %d characters in length '
                'and contain characters from 3 of the 4 categories: '
                'lowercase characters, uppercase characters, numbers '
                'and symbols.') % MIN_PASSWORD_LENGTH


class ChopRegistrationForm(EmailOnlyRegistrationForm):

    email = forms.EmailField(label=_('Email'),
                             help_text=_('If you are a CHOP employee, use your'
                                         ' CHOP-issued email address.'))

    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(render_value=False),
                                required=False, help_text=pw_help_text)

    password2 = forms.CharField(label=_('Confirm Password'),
                                widget=forms.PasswordInput(render_value=False),
                                required=False)

    institution = forms.CharField()
    reason = forms.CharField(widget=forms.Textarea)
    eula = forms.BooleanField()

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email').lower()
        if password and (email and not email.endswith('@email.chop.edu')):
            validate_password(password, length=MIN_PASSWORD_LENGTH)
        return password

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)

        # again, we do a custom setup for CHOP users
        if user.email.endswith('@email.chop.edu'):
            user.username = user.email.lower().split('@')[0]
            user.set_unusable_password()
        else:
            user.username = generate_random_username()
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            self.save_m2m()
        return user


class ChopPasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(label='Email',
                             help_text=_('If you are a CHOP employee, you must'
                                         ' use <a href="https://pwreset.'
                                         'chop.edu">this form</a> instead'))

    def clean_email(self):
        """
        Extended to check for CHOP emails.

        CHOP users cannot reset their passwords using this form.
        """
        email = super(ChopPasswordResetForm, self).clean_email()

        if email.endswith('@email.chop.edu'):
            raise forms.ValidationError(_('You cannot reset your password '
                                          'since this account is using your '
                                          'CHOP AD credentials.'))
        return email


class ChopSetPasswordForm(auth_forms.SetPasswordForm):
    "Password reset form, intended to be used for a non-authenticated user."
    new_password1 = forms.CharField(label=_('Password'),
                                    widget=forms.PasswordInput,
                                    help_text=pw_help_text)

    new_password2 = forms.CharField(label=_('Confirm Password'),
                                    widget=forms.PasswordInput)

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if password:
            validate_password(password, length=MIN_PASSWORD_LENGTH)
        return password


class BrpAuthenticationForm(auth_forms.AuthenticationForm):
    email = forms.CharField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    username = forms.CharField(required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # Fragile way of making sure people are using email addresses to log in.
	if email and '@' not in email:
            raise forms.ValidationError(_('Please use your CHOP issued email address (user@email.chop.edu)'))
        if email and password:
            # this is not a mistake.. Django assumes username will always be
            # used, but the auth backend accepts an email address
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_('Please enter a correct email '
                                              'and password. Note that both '
                                              'fields are case-sensitive.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is not active.'))
        self.check_for_test_cookie()
        return self.cleaned_data
