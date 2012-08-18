# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('blogs_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('blogs', ['Source'])

        # Adding model 'Blog'
        db.create_table('blogs_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blogs', to=orm['blogs.Source'])),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_domain', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identificator', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('blogs', ['Blog'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table('blogs_source')

        # Deleting model 'Blog'
        db.delete_table('blogs_blog')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blogs']