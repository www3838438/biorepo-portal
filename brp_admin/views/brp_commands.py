from django.views.generic import TemplateView
from django.shortcuts import render
from api.models.protocols import Protocol
from brp_admin.forms import ProtocolForm
from django.core import management

from django.http import HttpResponse


class CacheSubjects(TemplateView):

    def post(self, request):
        print(request)
        protocol = request.POST['protocol']
        if (protocol):
            management.call_command('cache_subjects', protocol, verbosity=0)
        else:
            management.call_command('cache_subjects', "all", verbosity=0)
        context = {}
        context['message'] = "Caching complete"
        return render(request, 'confirmation.html', context)

    def get(self, request):
        context = {}
        context['form_title'] = "Cache Subjects"
        context['message1'] = "select a protocol to cache subject in the protocol"
        context['message2'] = "This function may take a few minutes, you will receive confirmation shortly"
        context['form'] = ProtocolForm()
        return render(request, 'form.html', context)
