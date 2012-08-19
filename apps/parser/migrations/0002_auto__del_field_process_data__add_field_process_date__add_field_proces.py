# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Process.data'
        db.delete_column('parser_process', 'data')

        # Adding field 'Process.date'
        db.add_column('parser_process', 'date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 8, 19, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Process.hash'
        db.add_column('parser_process', 'hash',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Process.data'
        raise RuntimeError("Cannot reverse this migration. 'Process.data' and its values cannot be restored.")
        # Deleting field 'Process.date'
        db.delete_column('parser_process', 'date')

        # Deleting field 'Process.hash'
        db.delete_column('parser_process', 'hash')


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
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
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