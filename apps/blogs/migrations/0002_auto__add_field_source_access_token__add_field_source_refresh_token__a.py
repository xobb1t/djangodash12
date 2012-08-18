# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source.access_token'
        db.add_column('blogs_source', 'access_token',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Source.refresh_token'
        db.add_column('blogs_source', 'refresh_token',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Source.expiration_datetime'
        db.add_column('blogs_source', 'expiration_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 8, 18, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source.access_token'
        db.delete_column('blogs_source', 'access_token')

        # Deleting field 'Source.refresh_token'
        db.delete_column('blogs_source', 'refresh_token')

        # Deleting field 'Source.expiration_datetime'
        db.delete_column('blogs_source', 'expiration_datetime')


    models = {
        'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
            'default_domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blogs'", 'to': "orm['blogs.Source']"})
        },
        'blogs.source': {
            'Meta': {'object_name': 'Source'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expiration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blogs']