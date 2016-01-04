# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
	# Adding field 'Protocol.manage_research_ids'
	db.add_column(u'portal_protocol', 'manage_research_ids',
		      self.gf('django.db.models.fields.BooleanField')(default=False),
		      keep_default=False)


    def backwards(self, orm):
	# Deleting field 'Protocol.manage_research_ids'
	db.delete_column(u'portal_protocol', 'manage_research_ids')


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
	    'manage_research_ids': ('django.db.models.fields.BooleanField', [], {}),
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