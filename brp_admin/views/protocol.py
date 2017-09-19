import json

from django.contrib.auth.models import User
from api.models.protocols import ProtocolUser, ProtocolUserCredentials, Protocol, ProtocolDataSource

# from api.models.protocols import Protocol

from django.views.generic import TemplateView

from api.serializers import ProtocolSerializer
from api.views.protocol import ProtocolViewSet

from rest_framework.response import Response

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from brp_admin.forms import ProtocolUserForm, ProtocolUserCredentialsForm


class New_protocol_usr(TemplateView):

    template_name = 'new_protocol_usr.html'
    #
    # def get(self, request, *args, **kwargs):
    #
    #     serializer_context = {
    #         'request': request,
    #     }
    #     queryset = Protocol.objects.all()
    #     serializer_class = ProtocolSerializer(queryset, many=True, context=serializer_context)
    #     return Response(serializer_class.data, status=None, template_name=None, headers=None, content_type=None)

    def dispatch(self, request):

        if request.method == 'POST':
            post = request.POST

            print("printing request:")
            print(post)
            protocol_user = 'protocol_user' in post
            print(protocol_user)
            if 'protocol_user' in post:
                print("request.POST.get fn worked")
                protocolUserForm = ProtocolUserForm(data=request.POST)
                print("protocolUserForm valid?:")
                print(protocolUserForm.is_valid())
                if protocolUserForm.is_valid():
                    protocolUserForm.save()
                    print("is userform valid?")
                # get context data
                    context = {}
                    user = User.objects.get(pk=post['user'])
                    protocol = Protocol.objects.get(pk=post['protocol'])
                    context['user'] = user
                    context['protocol'] = protocol
                    credentials = ProtocolDataSource.objects.filter(protocol=protocol)
                    protocol_user = ProtocolUser.objects.get(protocol=protocol, user=post['user'])
                    # get all form needed for credentials
                    credential_forms = []
                    for item in credentials:
                        try:
                            user_credentials = ProtocolUserCredentials.objects.get(protocol=protocol, protocol_user=protocol_user, data_source=item)
                            try:
                                protocolCredentialsForm = ProtocolUserCredentialsForm(initial={'protocol': post['protocol'], 'protocol_user': protocol_user, 'data_source': item, 'data_source_username': user_credentials.data_source_username, 'data_source_password': user_credentials.data_source_password})
                            except:
                                pass
                        except:
                            protocolCredentialsForm = ProtocolUserCredentialsForm(initial={'protocol': post['protocol'], 'protocol_user': protocol_user, 'data_source': item})
                        credential_forms.append(protocolCredentialsForm)

                    context['credential_forms'] = credential_forms
                    print("context:")
                    print(context)
                    return render(request, 'protocol_user_credentials.html', {'context': context})
                    # return render(request, 'protocol_user_credentials.html', context)
                else:
                    context = {}
                    context['errors'] = protocolUserForm.errors
                    context['form1'] = protocolUserForm
                    print("are we getting to else? here are errors:")
                    print(context)
                    return render(request, 'new_protocol_usr.html', context)
                    '''
        * protocol = models.ForeignKey(Protocol, verbose_name='Protocol')
        * protocol_user = models.ForeignKey(
            ProtocolUser, verbose_name='Protocol User')
            '''
            if 'submit_creds' in post:
                    print("we arrived at password in post")

        protocolUserForm = ProtocolUserForm()
        return render(request, 'new_protocol_usr.html', {'form1': protocolUserForm})


class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
