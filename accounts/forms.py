from django import forms
from django.contrib.auth import forms as auth_forms, authenticate
from django.utils.translation import ugettext_lazy as _
from registration.forms import EmailOnlyRegistrationForm

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

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.username = user.email.lower().split('@')[0]
        user.set_unusable_password()

        if commit:
            user.save()
            self.save_m2m()
        return user


class BrpAuthenticationForm(auth_forms.AuthenticationForm):
    email = forms.CharField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    username = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # Fragile way of making sure people are using email addresses to log in.
        if email and password:
            # this is not a mistake.. Django assumes username will always be
            # used, but the auth backend accepts an email address
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_('Please enter a correct email '
                                              'and password. Note that both '
                                              'fields are case-sensitive.'))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_('This account is not active. Did you check your email to confirm registration?'))
        return self.cleaned_data
