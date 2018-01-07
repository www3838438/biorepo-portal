from django.forms import ModelForm
from django import forms
from api.models.protocols import ProtocolUserCredentials, ProtocolUser, Protocol
from django.contrib.auth.models import User


class ProtocolUserForm(ModelForm):
    class Meta:
        model = ProtocolUser
        fields = ('protocol', 'user', 'role')


class ProtocolUserCredentialsForm(ModelForm):
    ''' ProtocolUserCredential Model
    protocol = models.ForeignKey(Protocol, verbose_name='Protocol')
    data_source = models.ForeignKey(
        ProtocolDataSource, verbose_name='Protocol Data Source')
    user = models.ForeignKey(User, verbose_name='User')
    protocol_user = models.ForeignKey(
        ProtocolUser, verbose_name='Protocol User')
    data_source_username = models.CharField(
        max_length=50, verbose_name='Username for Data Source', blank=True)
    data_source_password = models.CharField(
        max_length=128, verbose_name='Password for Data Source')

    '''
    class Meta:
        model = ProtocolUserCredentials
        # fields = ('data_source', 'data_source_username', 'data_source_password')
        fields = ('__all__')


class ProtocolForm(forms.Form):
    protocol = forms.ModelChoiceField(queryset=Protocol.objects.all(), empty_label="All")


class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a User")
