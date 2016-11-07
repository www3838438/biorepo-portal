import socket
import logging

from django.http import HttpResponse, HttpResponseRedirect, Http404,\
    HttpResponseForbidden
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

log = logging.getLogger(__name__)


def forbidden(request, template_name='403.html'):
    '''Default 403 handler'''
    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))


def connectionRefused(func):
    def callfunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except socket.error:
            return HttpResponse('The system was unable to connect to either the eHB service or another datasource.')
    return callfunc

@login_required()
def index(request):
    usr = request.user
    token = ''
    if isinstance(usr, User):
        try:
            token = Token.objects.create(user=usr)
        except IntegrityError:
            token = Token.objects.get(user=usr)
    template = loader.get_template('index.html')
    context = {
        'request': request,
        'user': usr,
        'token': token,
    }
    return HttpResponse(template.render(context, request))

def changelog(request):
    f = open('CHANGELOG.md', 'rb')
    c_log = f.read()
    f.close()
    context = {
        'changelog': c_log,
        'version': 'v1.0.3'
    }
    template = loader.get_template('changelog.html')
    return HttpResponse(template.render(context, request))
