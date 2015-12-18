from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from accounts.forms import ChopPasswordResetForm, ChopSetPasswordForm

password_urls = patterns(
    'django.contrib.auth.views',
    url(r'^$', 'password_reset', {
        'password_reset_form': ChopPasswordResetForm,
    }, name='password-reset'),

    url(r'^send/$', 'password_reset_done', name='password-reset-sent'),

    url(r'^confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'password_reset_confirm', {
            'set_password_form': ChopSetPasswordForm,
        }, name='password-reset-confirm'),

    url(r'^complete/$', 'password_reset_complete',
        name='password-reset-complete'),
)

urlpatterns = patterns(
    '',
    url(r'^register/$', 'registration.views.register',
        name='register'),

    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration-complete'),

    url(r'^verify/(?P<activation_key>\w+)/$', 'registration.views.verify',
        name='verify-registration'),

    url(r'^moderate/(?P<activation_key>\w+)/$', 'registration.views.moderate',
        name='moderate-registration'),

    url(r'^moderate/$', 'registration.views.moderate_list',
        name='moderate-registration-list'),

    url(r'^password/reset/', include(password_urls)),

    url(r'^login/$', 'accounts.views.throttled_login', name='login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^eula/$', 'accounts.views.eula', name='eula'),
)
