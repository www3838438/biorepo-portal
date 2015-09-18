from django.db import models
from datetime import datetime


class CreatedModified(models.Model):
    date_help_text = "Please use date format: <em>YYYY-MM-DD</em>"
    created = models.DateTimeField(
	auto_now_add=True,
	verbose_name='Record Creation DateTime',
	help_text=date_help_text)
    modified = models.DateTimeField(
	auto_now_add=True,
	auto_now=True,
	verbose_name='Record Last Modified DateTime',
	help_text=date_help_text)

    class Meta(object):
        abstract = True

    def save(self):
        now = datetime.now()

        if not self.created:
            self.created = now

        self.modified = now

	super(CreatedModified, self).save()
