# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'School'
        db.create_table('CGL_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('KGS_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('club_president', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('captain', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('meeting_info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('CGL', ['School'])

        # Adding model 'Player'
        db.create_table('CGL_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('rank', self.gf('django.db.models.fields.IntegerField')(default=100, blank=True)),
            ('KGS_username', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.School'])),
            ('num_wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_losses', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('isActive', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('CGL', ['Player'])

        # Adding model 'Season'
        db.create_table('CGL_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('slug_name', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('schoolyear', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('CGL', ['Season'])

        # Adding model 'Membership'
        db.create_table('CGL_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.School'])),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.Season'])),
            ('num_wins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_losses', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_ties', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('CGL', ['Membership'])

        # Adding model 'Round'
        db.create_table('CGL_round', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.Season'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('CGL', ['Round'])

        # Adding model 'Match'
        db.create_table('CGL_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('round', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.Round'])),
            ('school1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='school1', to=orm['CGL.School'])),
            ('school2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='school2', to=orm['CGL.School'])),
            ('score1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('score2', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('CGL', ['Match'])

        # Adding model 'Game'
        db.create_table('CGL_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.Match'])),
            ('board', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gamefile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('white_school', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('school1_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_school1_player', to=orm['CGL.Player'])),
            ('school2_player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_school2_player', to=orm['CGL.Player'])),
        ))
        db.send_create_signal('CGL', ['Game'])

        # Adding model 'Forfeit'
        db.create_table('CGL_forfeit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.Match'])),
            ('board', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('forfeit', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('CGL', ['Forfeit'])

        # Adding model 'Newsfeed'
        db.create_table('CGL_newsfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('preview', self.gf('django.db.models.fields.TextField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('CGL', ['Newsfeed'])


    def backwards(self, orm):
        # Deleting model 'School'
        db.delete_table('CGL_school')

        # Deleting model 'Player'
        db.delete_table('CGL_player')

        # Deleting model 'Season'
        db.delete_table('CGL_season')

        # Deleting model 'Membership'
        db.delete_table('CGL_membership')

        # Deleting model 'Round'
        db.delete_table('CGL_round')

        # Deleting model 'Match'
        db.delete_table('CGL_match')

        # Deleting model 'Game'
        db.delete_table('CGL_game')

        # Deleting model 'Forfeit'
        db.delete_table('CGL_forfeit')

        # Deleting model 'Newsfeed'
        db.delete_table('CGL_newsfeed')


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
        'CGL.newsfeed': {
            'Meta': {'object_name': 'Newsfeed'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preview': ('django.db.models.fields.TextField', [], {}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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