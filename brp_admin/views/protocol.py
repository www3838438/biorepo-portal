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
        # post = get_object_or_404(ProtocolUserForm, pk=pk)
        # form = ProtocolUserForm()
        # print("we are getting to get request correct?")
        # return render(request, 'new_protocol_usr.html', {'form': form})


        # protocols = json.loads(Protocol.objects.all())
        # queryset = Protocol.objects.all()
        # serializer_class = ProtocolSerializer("json", queryset, many=True)
        # protocols = json.loads(serializer_class.initial_data)

        # protocols = []
        # for p in Protocol.objects.all():
        #     if request.user in p.users.all():
        #         protocols.append(ProtocolSerializer(p, context={'request': request}).data)

        ########## working ############
        # protocols = {}
        # protocols = Protocol.objects.all()
        #
        # print(protocols)
        # return render(request, 'new_protocol_usr.html', {'protocols': protocols})
        ################################
        if request.method == 'POST':
            post = request.POST
            protocolUserForm = ProtocolUserForm(data=request.POST)
            if protocolUserForm.is_valid():
                protocolUserForm.save()
            # get context data
            context = {}
            user = User.objects.get(pk=post['user'])
            protocol = Protocol.objects.get(pk=post['protocol'])
            context['user'] = user
            context['protocol'] = protocol
            # end get context data

            # json_context = json.dumps(context)


            # protocolCredentialsForm = ProtocolUserCredentialsForm(data=request.POST)
            # protocol = ProtocolUser(Protocol=protocolUserForm.cleaned_data['protocol'])
            # user = ProtocolUser(from_user=request.user)

            # protocolCredentialsForm = ProtocolUserCredentialsForm(data=request.POST, instance=protocol)
            # post.protocol = request.POST.protocol

            # todo: get list of datasources for given protocol.
            credentials = ProtocolDataSource.objects.filter(protocol=protocol)
            print("credentials:")
            print(credentials)
            print("****** end of cred *******")
            credential_forms = []

            for item in credentials:
                protocolCredentialsForm = ProtocolUserCredentialsForm(initial={'protocol': post['protocol'], 'protocol_user': post['user'], 'data_source': item})
                credential_forms.append(protocolCredentialsForm)
                print(item.data_source)

            context['credential_forms'] = credential_forms
            print ("printing context")
            print (context)
            print ("***** end of context *******")
            return render(request, 'protocol_user_credentials.html', {'context': context})

            # if protocolCredentialsForm.is_valid():
            #     protocolCredentialsForm.save()




        '''
        * protocol = models.ForeignKey(Protocol, verbose_name='Protocol')
        * protocol_user = models.ForeignKey(
            ProtocolUser, verbose_name='Protocol User')
            '''
        protocolUserForm = ProtocolUserForm()
        # protocolCredentialsForm = ProtocolUserCredentialsForm()
        return render(request, 'new_protocol_usr.html', {'form1': protocolUserForm})

    def post(self, request):
        pass


    # def protocols(self):
    #     return Protocol.objects.all()

    # def users(self):
    #     return User.objects.all()


class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
