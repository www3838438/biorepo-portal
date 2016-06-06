import socket
import json
import logging

from django.http import HttpResponse, HttpResponseRedirect, Http404,\
    HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.template import loader
# from portal.forms.subject_forms import NewSubjectForm, EditSubjectForm
# from portal.ehb_service_client import ServiceClient
from api.models.protocols import Protocol, ProtocolDataSource,\
    Organization, ProtocolUserCredentials, ProtocolDataSourceLink
# from portal.utilities import SubjectUtils, DriverUtils
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
#
# from ehb_client.requests.exceptions import ErrorConstants, PageNotFound
# from ehb_client.requests.base import RequestBase
# from ehb_client.requests.external_record_request_handler import ExternalRecord
# from ehb_client.requests.subject_request_handler import Subject
# from ehb_datasources.drivers.exceptions import RecordDoesNotExist,\
#     RecordCreationError, IgnoreEhbExceptions

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
