from django.contrib.auth.decorators import login_required
from portal.models.protocols import Protocol
from django.template import RequestContext
from django.shortcuts import render_to_response
from portal.ehb_service_client import ServiceClient


def index(request):
    usr = request.user
    return render_to_response('base.html')
