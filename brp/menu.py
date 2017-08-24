"""

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'biorepo-portal.menu.CustomMenu'
"""

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for biorepo-portal admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.AppList(
                _('Models'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.MenuItem(
                _('Protocol Management'),
                children=[
                    items.MenuItem('add user to protocol', '/foo/'),
                    items.MenuItem('Add Data Source to protocol', '/bar/'),
                ]
            ),
            items.MenuItem(
                _('BRP Management'),
                children=[
                    items.MenuItem('re-activate user', '/foo/'),
                    items.MenuItem('cache subjects', '/bar/'),
                    items.MenuItem('toggle maintenance', '/bar/'),
                ]
            ),
            items.MenuItem(
                _('BRP/EHB Useful links'),
                children=[
                    items.MenuItem('BRP EHB Gist', '/foo/'),
                    items.MenuItem('BRP read the docs', '/bar/'),
                    items.MenuItem('BRP user guide', '/bar/'),
                    items.MenuItem('BRP CHOP wiki', '/bar/'),
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
