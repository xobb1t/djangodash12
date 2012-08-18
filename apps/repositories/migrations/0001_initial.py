# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('repositories_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identification', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('repositories', ['User'])

        # Adding model 'Repo'
        db.create_table('repositories_repo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='repos', to=orm['repositories.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cname', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('repositories', ['Repo'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('repositories_user')

        # Deleting model 'Repo'
        db.delete_table('repositories_repo')


    models = {
        'repositories.repo': {
            'Meta': {'object_name': 'Repo'},
            'cname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'repos'", 'to': "orm['repositories.User']"})
        },
        'repositories.user': {
            'Meta': {'object_name': 'User'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identification': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['repositories']