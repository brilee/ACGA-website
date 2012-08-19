# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Newsfeed'
        db.delete_table('CGL_newsfeed')


    def backwards(self, orm):
        # Adding model 'Newsfeed'
        db.create_table('CGL_newsfeed', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('preview', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('CGL', ['Newsfeed'])


    models = {
        'CGL.forfeit': {
            'Meta': {'ordering': "['-match__round__date', 'board']", 'object_name': 'Forfeit'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'forfeit': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"})
        },
        'CGL.game': {
            'Meta': {'ordering': "['-match__round__date', 'board']", 'object_name': 'Game'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gamefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"}),
            'school1_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school1_player'", 'to': "orm['CGL.Player']"}),
            'school2_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school2_player'", 'to': "orm['CGL.Player']"}),
            'white_school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'CGL.match': {
            'Meta': {'object_name': 'Match'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Round']"}),
            'school1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school1'", 'to': "orm['CGL.School']"}),
            'school2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school2'", 'to': "orm['CGL.School']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'CGL.membership': {
            'Meta': {'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"})
        },
        'CGL.player': {
            'KGS_username': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'Meta': {'ordering': "['school', 'name', 'rank']", 'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '100', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'CGL.round': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Round'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"})
        },
        'CGL.school': {
            'KGS_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'Meta': {'ordering': "['name']", 'object_name': 'School'},
            'captain': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'club_president': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'CGL.season': {
            'Meta': {'object_name': 'Season'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['CGL.School']", 'through': "orm['CGL.Membership']", 'symmetrical': 'False'}),
            'schoolyear': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['CGL']