# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Process'
        db.create_table('parser_process', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blogs.Blog'], unique=True)),
            ('repo', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['repositories.Repo'], unique=True)),
            ('stage', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('error', self.gf('django.db.models.fields.TextField')()),
            ('data', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('parser', ['Process'])


    def backwards(self, orm):
        # Deleting model 'Process'
        db.delete_table('parser_process')


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
        },
        'parser.process': {
            'Meta': {'object_name': 'Process'},
            'blog': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blogs.Blog']", 'unique': 'True'}),
            'data': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['repositories.Repo']", 'unique': 'True'}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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