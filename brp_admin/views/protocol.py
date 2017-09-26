from django.contrib.auth.models import User
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource

from django.views.generic import TemplateView


from django.shortcuts import render

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm

from django.forms.formsets import formset_factory

class New_protocol_usr(TemplateView):

    template_name = 'new_protocol_usr.html'

    def dispatch(self, request):

        credential_form_set = (formset_factory(ProtocolUserCredentialsForm, can_delete=True, extra=0))

        if request.method == 'POST':
            post = request.POST

            protocol_user = 'protocol_user' in post

            if 'protocol_user' in post or 'get_credentials' in post:

                protocolUserForm = ProtocolUserForm(data=request.POST)

                if protocolUserForm.is_valid():
                    protocolUserForm.save()
                    print("is userform valid?")

                if not protocolUserForm.is_valid() and 'protocol_user' in post:
                    context = {}
                    context['errors'] = protocolUserForm.errors
                    context['form1'] = protocolUserForm
                    print("are we getting to else? here are errors:")
                    print(context)
                    return render(request, 'new_protocol_usr.html', context)
                # get context data
                context = {}
                user = User.objects.get(pk=post['user'])
                protocol = Protocol.objects.get(pk=post['protocol'])
                context['user'] = user
                context['protocol'] = protocol
                empty_credentials = ProtocolDataSource.objects.filter(protocol=protocol)
                protocol_user = ProtocolUser.objects.get(protocol=protocol, user=post['user'])

                if 'protocol_user' in post:
                    credential_data = [{'protocol': protocol,
                                        'data_source': item,
                                        'user': user,
                                        'protocol_user': protocol_user}
                                       for item in empty_credentials]
                if 'get_credentials' in post:

                    credentials = ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user)
                    if not protocol_user:
                        print("we are getting into error")
                        context['error'] = " please add user to protocol"
                        return render(request, 'new_protocol_usr.html', {'context': context})
                    if not credentials:
                        print("wer are getting into not credentials")
                        credential_data = [{'protocol': protocol,
                                            'data_source': item,
                                            'user': user,
                                            'protocol_user': protocol_user}
                                           for item in empty_credentials]
                    else:
                        credential_data = [{'protocol': post['protocol'],
                                            'protocol_user': protocol_user,
                                            'user': user,
                                            'data_source': cred.data_source,
                                            'data_source_username': cred.data_source_username,
                                            'data_source_password': cred.data_source_password}
                                           for cred in credentials]

                credential_form_set = (formset_factory(ProtocolUserCredentialsForm, can_delete=True, extra=0))

                credential_formSet = credential_form_set(initial=credential_data)
                context['cred_formset'] = credential_formSet
                return render(request, 'protocol_user_credentials.html', {'context': context})

            if 'submit_creds' in post:
                context = {}
                message = 'credentials not saved'
                credentials = []
                cred_formset = credential_form_set(post)
                for cred_form in cred_formset:
                    if cred_form.has_changed() and cred_form.is_valid():
                        cred_form.save()

                        context['data_source'] = cred_form
                        message = 'credentials saved'

                context['message'] = message
                return render(request, 'confirmation.html', context)

        protocolUserForm = ProtocolUserForm()
        return render(request, 'new_protocol_usr.html', {'form1': protocolUserForm})


class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
