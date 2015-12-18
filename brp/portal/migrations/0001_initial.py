# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
	# Adding model 'ImmutableKey'
	db.create_table(u'portal_immutablekey', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, blank=True)),
	))
	db.send_create_signal(u'portal', ['ImmutableKey'])

	# Adding model 'Organization'
	db.create_table(u'portal_organization', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('immutable_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.ImmutableKey'], unique=True, null=True, blank=True)),
	    ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
	    ('subject_id_label', self.gf('django.db.models.fields.CharField')(default='Record ID', max_length=50)),
	))
	db.send_create_signal(u'portal', ['Organization'])

	# Adding model 'DataSource'
	db.create_table(u'portal_datasource', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
	    ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=255)),
	    ('description', self.gf('django.db.models.fields.TextField')()),
	    ('ehb_service_es_id', self.gf('django.db.models.fields.IntegerField')(default=-1)),
	))
	db.send_create_signal(u'portal', ['DataSource'])

	# Adding model 'Protocol'
	db.create_table(u'portal_protocol', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('immutable_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.ImmutableKey'], unique=True, null=True, blank=True)),
	    ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
	))
	db.send_create_signal(u'portal', ['Protocol'])

	# Adding M2M table for field organizations on 'Protocol'
	m2m_table_name = db.shorten_name(u'portal_protocol_organizations')
	db.create_table(m2m_table_name, (
	    ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
	    ('protocol', models.ForeignKey(orm[u'portal.protocol'], null=False)),
	    ('organization', models.ForeignKey(orm[u'portal.organization'], null=False))
	))
	db.create_unique(m2m_table_name, ['protocol_id', 'organization_id'])

	# Adding model 'ProtocolDataSource'
	db.create_table(u'portal_protocoldatasource', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(related_name='protocol_data_sources', to=orm['portal.Protocol'])),
	    ('data_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.DataSource'])),
	    ('path', self.gf('django.db.models.fields.CharField')(max_length=255)),
	    ('driver', self.gf('django.db.models.fields.IntegerField')()),
	    ('driver_configuration', self.gf('django.db.models.fields.TextField')(blank=True)),
	    ('display_label', self.gf('django.db.models.fields.CharField')(max_length=50)),
	    ('max_records_per_subject', self.gf('django.db.models.fields.IntegerField')(default=-1)),
	))
	db.send_create_signal(u'portal', ['ProtocolDataSource'])

	# Adding model 'ProtocolDataSourceLink'
	db.create_table(u'portal_protocoldatasourcelink', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('pds_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pds_one_set', to=orm['portal.ProtocolDataSource'])),
	    ('pds_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pds_two_set', to=orm['portal.ProtocolDataSource'])),
	    ('linker', self.gf('django.db.models.fields.CharField')(max_length=200)),
	))
	db.send_create_signal(u'portal', ['ProtocolDataSourceLink'])

	# Adding model 'ProtocolUser'
	db.create_table(u'portal_protocoluser', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Protocol'])),
	    ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
	    ('role', self.gf('django.db.models.fields.IntegerField')()),
	))
	db.send_create_signal(u'portal', ['ProtocolUser'])

	# Adding unique constraint on 'ProtocolUser', fields ['protocol', 'user']
	db.create_unique(u'portal_protocoluser', ['protocol_id', 'user_id'])

	# Adding model 'ProtocolUserCredentials'
	db.create_table(u'portal_protocolusercredentials', (
	    (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
	    ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
	    ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
	    ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.Protocol'])),
	    ('data_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.ProtocolDataSource'])),
	    ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
	    ('protocol_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portal.ProtocolUser'])),
	    ('data_source_username', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
	    ('data_source_password', self.gf('django.db.models.fields.CharField')(max_length=128)),
	    ('allow_label_printing', self.gf('django.db.models.fields.BooleanField')(default=False)),
	    ('allow_zpl_export', self.gf('django.db.models.fields.BooleanField')(default=False)),
	    ('allow_chop_printing', self.gf('django.db.models.fields.BooleanField')(default=False)),
	))
	db.send_create_signal(u'portal', ['ProtocolUserCredentials'])

	# Adding unique constraint on 'ProtocolUserCredentials', fields ['data_source', 'user', 'protocol']
	db.create_unique(u'portal_protocolusercredentials', ['data_source_id', 'user_id', 'protocol_id'])


    def backwards(self, orm):
	# Removing unique constraint on 'ProtocolUserCredentials', fields ['data_source', 'user', 'protocol']
	db.delete_unique(u'portal_protocolusercredentials', ['data_source_id', 'user_id', 'protocol_id'])

	# Removing unique constraint on 'ProtocolUser', fields ['protocol', 'user']
	db.delete_unique(u'portal_protocoluser', ['protocol_id', 'user_id'])

	# Deleting model 'ImmutableKey'
	db.delete_table(u'portal_immutablekey')

	# Deleting model 'Organization'
	db.delete_table(u'portal_organization')

	# Deleting model 'DataSource'
	db.delete_table(u'portal_datasource')

	# Deleting model 'Protocol'
	db.delete_table(u'portal_protocol')

	# Removing M2M table for field organizations on 'Protocol'
	db.delete_table(db.shorten_name(u'portal_protocol_organizations'))

	# Deleting model 'ProtocolDataSource'
	db.delete_table(u'portal_protocoldatasource')

	# Deleting model 'ProtocolDataSourceLink'
	db.delete_table(u'portal_protocoldatasourcelink')

	# Deleting model 'ProtocolUser'
	db.delete_table(u'portal_protocoluser')

	# Deleting model 'ProtocolUserCredentials'
	db.delete_table(u'portal_protocolusercredentials')


    models = {
	u'auth.group': {
	    'Meta': {'object_name': 'Group'},
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
	    'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
	},
	u'auth.permission': {
	    'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
	    'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
	    'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
	},
	u'auth.user': {
	    'Meta': {'object_name': 'User'},
	    'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
	    'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
	    'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
	    'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
	    'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
	    'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
	    'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
	    'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
	    'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
	    'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
	    'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
	},
	u'contenttypes.contenttype': {
	    'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
	    'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
	    'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
	},
	u'portal.datasource': {
	    'Meta': {'object_name': 'DataSource'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    'description': ('django.db.models.fields.TextField', [], {}),
	    'ehb_service_es_id': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
	    'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255'})
	},
	u'portal.immutablekey': {
	    'Meta': {'object_name': 'ImmutableKey'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
	},
	u'portal.organization': {
	    'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'immutable_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.ImmutableKey']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
	    'subject_id_label': ('django.db.models.fields.CharField', [], {'default': "'Record ID'", 'max_length': '50'})
	},
	u'portal.protocol': {
	    'Meta': {'ordering': "['name']", 'object_name': 'Protocol'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    'data_sources': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['portal.DataSource']", 'through': u"orm['portal.ProtocolDataSource']", 'symmetrical': 'False'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'immutable_key': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.ImmutableKey']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
	    'organizations': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['portal.Organization']", 'symmetrical': 'False', 'blank': 'True'}),
	    'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False', 'through': u"orm['portal.ProtocolUser']", 'blank': 'True'})
	},
	u'portal.protocoldatasource': {
	    'Meta': {'ordering': "['protocol']", 'object_name': 'ProtocolDataSource'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    'data_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.DataSource']"}),
	    'display_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
	    'driver': ('django.db.models.fields.IntegerField', [], {}),
	    'driver_configuration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'max_records_per_subject': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
	    'protocol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'protocol_data_sources'", 'to': u"orm['portal.Protocol']"})
	},
	u'portal.protocoldatasourcelink': {
	    'Meta': {'object_name': 'ProtocolDataSourceLink'},
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'linker': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
	    'pds_one': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pds_one_set'", 'to': u"orm['portal.ProtocolDataSource']"}),
	    'pds_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pds_two_set'", 'to': u"orm['portal.ProtocolDataSource']"})
	},
	u'portal.protocoluser': {
	    'Meta': {'ordering': "['user']", 'unique_together': "(('protocol', 'user'),)", 'object_name': 'ProtocolUser'},
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.Protocol']"}),
	    'role': ('django.db.models.fields.IntegerField', [], {}),
	    'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
	},
	u'portal.protocolusercredentials': {
	    'Meta': {'ordering': "['protocol']", 'unique_together': "(('data_source', 'user', 'protocol'),)", 'object_name': 'ProtocolUserCredentials'},
	    'allow_chop_printing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
	    'allow_label_printing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
	    'allow_zpl_export': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
	    'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
	    'data_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.ProtocolDataSource']"}),
	    'data_source_password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
	    'data_source_username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
	    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	    'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
	    'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.Protocol']"}),
	    'protocol_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portal.ProtocolUser']"}),
	    'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
	}
    }

    complete_apps = ['portal']
