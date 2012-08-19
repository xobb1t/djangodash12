# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Blog.default_domain'
        db.delete_column('blogs_blog', 'default_domain')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Blog.default_domain'
        raise RuntimeError("Cannot reverse this migration. 'Blog.default_domain' and its values cannot be restored.")

    models = {
        'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
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
            'identificator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'blogger'", 'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blogs']