from django.contrib.auth.decorators import login_required
from portal.models.protocols import Protocol
from django.template import RequestContext
from django.shortcuts import render_to_response
from portal.ehb_service_client import ServiceClient


def index(request):
    usr = request.user
    return render_to_response('base.html')


def welcome(request):
    protocols = []
    # find the protocols for this user
    usr = request.user
    for p in Protocol.objects.all():
        if request.user in p.users.all():
            protocols.append(p)
    return render_to_response('welcome.html',
                              {
                                'user': usr,
                                'protocols': protocols,
                                'root_path': ServiceClient.self_root_path
                              }, context_instance=RequestContext(request))
