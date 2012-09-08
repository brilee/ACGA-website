# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table('ACGA_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('upload', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ACGA', ['Document'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table('ACGA_document')


    models = {
        'ACGA.document': {
            'Meta': {'object_name': 'Document'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ACGA.newsfeed': {
            'Meta': {'object_name': 'Newsfeed'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preview': ('django.db.models.fields.TextField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ACGA']