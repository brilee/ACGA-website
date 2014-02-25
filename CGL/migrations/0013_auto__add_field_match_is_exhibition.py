# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Match.is_exhibition'
        db.add_column('CGL_match', 'is_exhibition',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Match.is_exhibition'
        db.delete_column('CGL_match', 'is_exhibition')


    models = {
        'CGL.bye': {
            'Meta': {'ordering': "['-round__date']", 'object_name': 'Bye'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Round']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"})
        },
        'CGL.forfeit': {
            'Meta': {'ordering': "['-match__round__date', 'board']", 'object_name': 'Forfeit'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"}),
            'school1_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school2_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'CGL.game': {
            'Meta': {'ordering': "['-match__round__date', 'match__school1__name', 'board']", 'object_name': 'Game'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gamefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Match']"}),
            'school1_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school1_player'", 'to': "orm['CGL.Player']"}),
            'school2_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school2_player'", 'to': "orm['CGL.Player']"}),
            'white_school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'winning_school': ('django.db.models.fields.CharField', [], {'max_length': '10'})
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
            'school1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school1'", 'to': "orm['CGL.School']"}),
            'school2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school2'", 'to': "orm['CGL.School']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'CGL.membership': {
            'Meta': {'ordering': "['-season__pk', '-num_wins', 'num_losses', '-num_ties', 'num_forfeits']", 'object_name': 'Membership'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_byes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_forfeits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.School']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"}),
            'still_participating': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['CGL.Season']"})
        },
        'CGL.school': {
            'KGS_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'Meta': {'ordering': "['name']", 'object_name': 'School'},
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
        'CGL.season': {
            'Meta': {'object_name': 'Season'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['CGL.School']", 'through': "orm['CGL.Membership']", 'symmetrical': 'False'}),
            'schoolyear': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
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