# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration, DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):

        db.create_table(u'accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(null=False)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('eula', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        "Perform a 'safe' load using Avocado's backup utilities."
        from django.core.management import call_command
        call_command('loaddata', 'brp/apps/accounts/fixtures/0001_eula.json')

    def backwards(self, orm):
        db.delete_table(u'accounts_userprofile')
