from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource


class ProtocolUserView(TemplateView):

    template_name = 'new_protocol_usr.html'

    def __init__(self):
        self.protocol_user_form = ProtocolUserForm()

    def processProtocolUserForm(self, request):

        post_info = request.POST
        protocolUserForm = ProtocolUserForm(data=request.POST)
        self.protocol = post_info['protocol']
        self.user = post_info['user']
        try:
            self.protocol_user = ProtocolUser.objects.get(protocol=self.protocol, user=self.user)
        except(ObjectDoesNotExist):
            pass

        # if form is valid save
        if protocolUserForm.is_valid():
            protocolUserForm.save()
            self.protocol_user = ProtocolUser.objects.get(protocol=post_info['protocol'], user=post_info['user'])
        # to do: if errors send to UI

    def get(self, request):
        return render(request, 'new_protocol_usr.html', {'form1': ProtocolUserForm()})

    def post(self, request):
        post_data = request.POST

        if 'submit_creds' in post_data:
            return ProtocolUserCredentialForm.as_view()(self.request)

        self.processProtocolUserForm(request)

        return ProtocolUserCredentialForm.as_view()(self.request)


class ProtocolUserCredentialForm(TemplateView):

    def getCred_formset(self, protocol, protocol_user, user):
        credentials = ''
        try:
            credentials = ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user)
            credential_data = [{'protocol': protocol,
                                'protocol_user': protocol_user,
                                'user': user,
                                'data_source': cred.data_source,
                                'data_source_username': cred.data_source_username,
                                'data_source_password': cred.data_source_password}
                               for cred in credentials]

        except(ObjectDoesNotExist):
            pass

        if (credentials):
            credential_form_set = (modelformset_factory(
                ProtocolUserCredentials,
                fields='__all__',
                can_delete=True,
                extra=0))
            self.credential_form_set = credential_form_set

            return credential_form_set(queryset=ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user))
        else:
            empty_credentials = ProtocolDataSource.objects.filter(protocol=protocol)
            credential_data = [{'protocol': protocol,
                                'data_source': item,
                                'user': user,
                                'protocol_user': protocol_user}
                               for item in empty_credentials]
            credential_form_set = (formset_factory(
                ProtocolUserCredentialsForm,
                can_delete=True,
                extra=0))
            # self.setCredentialFormSet(credential_form_set)
            self.credential_form_set = credential_form_set
            return credential_form_set(initial=credential_data)

    def getCredFormInstance(self, protocol_user, protocol, user, data_source):
        try:
            return ProtocolUserCredentials.objects.get(
                protocol=protocol,
                data_source=data_source,
                user=user)
        except(ObjectDoesNotExist):
            pass
        return ''

    def processProtocolUserCredForm(self, request):
        context = {}
        context['message'] = 'credentials not saved'
        cred_formset = self.credential_form_set(request.POST)
        for cred_form in cred_formset:
            if cred_form.has_changed() and cred_form.is_valid():
                cred_form.save()


                # get changes and send to confirmation page
            # todo: if errors send to UI
                context['data_source'] = cred_form
                message = 'credentials saved'

        context['message'] = message

    def get_context_data(self, request):
        request_info = request.POST
        user = request_info['user']
        protocol = request_info['protocol']
        protocol_user = ProtocolUser.objects.get(protocol=protocol, user=user)

        context = {}

        context['cred_formset'] = self.getCred_formset(protocol,
                                                       protocol_user,
                                                       user)
        context['user'] = User.objects.get(pk=user)
        context['protocol'] = Protocol.objects.get(pk=protocol)
        return context

    def get(self, request):
        pass

    def post(self, request):
        post_data = request.POST

        if 'submit_creds' in post_data:
            user = post_data['form-0-user']
            protocol = post_data['form-0-protocol']
            protocol_user = ProtocolUser.objects.get(protocol=protocol, user=user)
            self.getCred_formset(protocol, protocol_user, user)
            self.processProtocolUserCredForm(request)
            context = {}
            context['message'] = "credentials saved"
            return render(request, 'confirmation.html', context)

        else:
            context = self.get_context_data(request)
            return render(request, 'protocol_user_credentials.html', context)


class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
