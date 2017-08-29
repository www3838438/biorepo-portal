from django.contrib.auth.models import User

from api.models.protocols import Protocol

from django.views.generic import TemplateView


class New_protocol_usr(TemplateView):

    template_name = 'new_protocol_usr.html'

    def protocols(self):
        return Protocol.objects.all()

    def users(self):
        return User.objects.all()

class Fn_in_progress(TemplateView):

    template_name = 'in_progress.html'
