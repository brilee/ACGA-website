# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchoolAuth'
        db.create_table('CGL_schoolauth', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['CGL.School'])),
            ('secret_key', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('CGL', ['SchoolAuth'])


    def backwards(self, orm):
        # Deleting model 'SchoolAuth'
        db.delete_table('CGL_schoolauth')


    models = {
        'CGL.bye': {
            'Meta': {'ordering': "['-round__date']", 'object_name': 'Bye'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Round']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Team']", 'null': 'True'})
        },
        'CGL.forfeit': {
            'Meta': {'ordering': "['-match__round__date', 'board']", 'object_name': 'Forfeit'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"}),
            'team1_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team2_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'CGL.game': {
            'Meta': {'ordering': "['-match__round__date', 'match__team1__school__name', 'board']", 'object_name': 'Game'},
            'black_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black_player_game_set'", 'null': 'True', 'to': "orm['CGL.Player']"}),
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'game_result': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10', 'blank': 'True'}),
            'gamefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'handicap': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"}),
            'white_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'white_player_game_set'", 'null': 'True', 'to': "orm['CGL.Player']"}),
            'white_school': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'CGL.gamecomment': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'GameComment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'CGL.match': {
            'Meta': {'ordering': "['-round__date']", 'object_name': 'Match'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exhibition': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Round']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score2': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team1'", 'null': 'True', 'to': "orm['CGL.Team']"}),
            'team2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'team2'", 'null': 'True', 'to': "orm['CGL.Team']"})
        },
        'CGL.player': {
            'KGS_username': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'Meta': {'ordering': "['school', 'name', 'rank']", 'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'receiveSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'CGL.round': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Round'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"})
        },
        'CGL.school': {
            'KGS_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'Meta': {'ordering': "['name']", 'object_name': 'School'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'captain': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'club_president': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inCGL': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meeting_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'CGL.schoolauth': {
            'Meta': {'object_name': 'SchoolAuth'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'CGL.season': {
            'Meta': {'object_name': 'Season'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['CGL.School']", 'through': "orm['CGL.Team']", 'symmetrical': 'False'}),
            'schoolyear': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'CGL.team': {
            'Meta': {'ordering': "['-season__pk', '-num_wins', 'num_losses', '-num_ties', 'num_forfeits']", 'object_name': 'Team', 'db_table': "'CGL_membership'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_byes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_forfeits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"}),
            'still_participating': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['CGL']