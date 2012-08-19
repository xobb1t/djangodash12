# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Process.stage'
        db.add_column('parser_process', 'stage',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Process.stage'
        db.delete_column('parser_process', 'stage')


    models = {
        'blogs.blog': {
            'Meta': {'object_name': 'Blog'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blogs'", 'to': "orm['blogs.Source']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'blogs.source': {
            'Meta': {'object_name': 'Source'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'expiration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'blogger'", 'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'parser.process': {
            'Meta': {'object_name': 'Process'},
            'blog': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blogs.Blog']", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['repositories.Repo']", 'unique': 'True'}),
            'stage': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'repositories.repo': {
            'Meta': {'object_name': 'Repo'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repos'", 'to': "orm['blogs.Blog']"}),
            'cname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repos'", 'to': "orm['repositories.User']"})
        },
        'repositories.user': {
            'Meta': {'object_name': 'User'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['parser']