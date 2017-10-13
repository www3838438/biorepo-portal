from django.contrib.auth.models import User
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource

from django.views.generic import TemplateView


from django.shortcuts import render

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm

from django.forms.formsets import formset_factory

class New_protocol_usr(TemplateView):

    template_name = 'new_protocol_usr.html'

    # this function will process a form that is in a post request
    def process_form(self, request, form):
        self.context = {}
        form_to_process = form(data=request.POST)
        if form_to_process.is_valid():
            form_to_process.save()
            self.context['errors_boolean'] = 'false'
        else:
            self.context['errors_boolean'] = 'true'
            self.context['errors'] = form_to_process.errors
            self.context['form'] = form_to_process
        print('context at end of process_form:')
        print(self.context)
    # def get_context_data(self, request):
    #     context = {}

    def dispatch(self, request):

        credential_form_set = (formset_factory(ProtocolUserCredentialsForm, can_delete=True, extra=0))

        if request.method == 'POST':
            post = request.POST
            print('post just after if request.method == POST')
            print(post)

            protocol_user = 'protocol_user' in post

            # if user selects 'add user to protocol' or 'Get protocol user Credentials'
            # check to make sure all fields are filled out before processing.
            if 'add_protocol_user' in post or 'get_credentials' in post:

                # context = {}

                self.process_form(request, ProtocolUserForm)

                # protocolUserForm = ProtocolUserForm(data=request.POST)

                # if protocolUserForm.is_valid():
                #     protocolUserForm.save()
                #     print("is userform valid?")
                print('context line 50:')
                print(self.context)
                if self.context['errors_boolean'] == 'true' and 'add_protocol_user' in post:

                    # context['errors'] = protocolUserForm.errors
                    # context['form1'] = protocolUserForm
                    print("are we getting to else? here are errors:")
                    print(self.context)
                    return render(request, 'new_protocol_usr.html', self.context)
                # get context data
                context = {}
                user = User.objects.get(pk=post['user'])
                protocol = Protocol.objects.get(pk=post['protocol'])
                context['user'] = user
                context['protocol'] = protocol
                empty_credentials = ProtocolDataSource.objects.filter(protocol=protocol)
                try:
                    protocol_user = ProtocolUser.objects.get(protocol=protocol, user=post['user'])
                except:
                    protocol_user = 'false'

                # if we just added a user to the protocol we want to render all
                # credential datasouces available for given protocol.
                if 'add_protocol_user' in post:
                    credential_data = [{'protocol': protocol,
                                        'data_source': item,
                                        'user': user,
                                        'protocol_user': protocol_user}
                                       for item in empty_credentials]
                # if we are getting credentials for users that were already
                # added to protocol we want to render credentals already in
                # database.
                if 'get_credentials' in post:

                    credentials = ProtocolUserCredentials.objects.filter(protocol=protocol, protocol_user=protocol_user)
                    # if user is not added to protocol we want to render
                    # protocolUserForm so admin user and add user to protocol.
                    if not protocol_user:
                        print("we are getting into error")
                        context['errors'] = " please add user to protocol"
                        return render(request, 'new_protocol_usr.html', context)
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
        return render(request, 'new_protocol_usr.html', {'form': protocolUserForm})


class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
