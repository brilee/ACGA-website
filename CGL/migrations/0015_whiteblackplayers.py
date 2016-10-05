# -*- coding: utf-8 -*-
from south.v2 import DataMigration

class Migration(DataMigration):
    SCHOOL1, SCHOOL2 = 'School1', 'School2'

    def forwards(self, orm):
        "Write your forwards methods here."
        for game in orm.Game.objects.all():
            if game.white_school == self.SCHOOL1:
                game.white_player = game.school1_player
                game.black_player = game.school2_player
            elif game.white_school == self.SCHOOL2:
                game.black_player = game.school1_player
                game.white_player = game.school2_player
            else:
                raise Exception('Failed to specify school choices properly...')
            game.save()
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        for game in orm.Game.objects.all():
            if game.white_school == self.SCHOOL1:
                game.school1_player = game.white_player
                game.school2_player = game.black_player
            elif game.white_school == self.SCHOOL2:
                game.school2_player = game.white_player
                game.school1_player = game.black_player
            else:
                raise Exception('Failed to specify school choices properly...')
            game.save()


    models = {
        u'CGL.bye': {
            'Meta': {'ordering': "['-round__date']", 'object_name': 'Bye'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Round']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.School']"})
        },
        u'CGL.forfeit': {
            'Meta': {'ordering': "['-match__round__date', 'board']", 'object_name': 'Forfeit'},
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Match']"}),
            'school1_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school2_noshow': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'CGL.game': {
            'Meta': {'ordering': "['-match__round__date', 'match__school1__name', 'board']", 'object_name': 'Game'},
            'black_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'black_player'", 'null': 'True', 'to': u"orm['CGL.Player']"}),
            'board': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gamefile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Match']"}),
            'school1_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school1_player'", 'to': u"orm['CGL.Player']"}),
            'school2_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_school2_player'", 'to': u"orm['CGL.Player']"}),
            'white_player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'white_player'", 'null': 'True', 'to': u"orm['CGL.Player']"}),
            'white_school': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'winning_school': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'CGL.gamecomment': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'GameComment'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'CGL.match': {
            'Meta': {'ordering': "['-round__date']", 'object_name': 'Match'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exhibition': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'round': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Round']"}),
            'school1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school1'", 'to': u"orm['CGL.School']"}),
            'school2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school2'", 'to': u"orm['CGL.School']"}),
            'score1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'score2': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'CGL.membership': {
            'Meta': {'ordering': "['-season__pk', '-num_wins', 'num_losses', '-num_ties', 'num_forfeits']", 'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_byes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_forfeits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_ties': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.School']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Season']"}),
            'still_participating': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'CGL.player': {
            'KGS_username': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'Meta': {'ordering': "['school', 'name', 'rank']", 'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isActive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'num_losses': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_wins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'receiveSpam': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.School']"}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'CGL.round': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Round'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['CGL.Season']"})
        },
        u'CGL.school': {
            'KGS_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'Meta': {'ordering': "['name']", 'object_name': 'School'},
            'captain': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'club_president': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inCGL': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'meeting_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'CGL.season': {
            'Meta': {'object_name': 'Season'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['CGL.School']", 'through': u"orm['CGL.Membership']", 'symmetrical': 'False'}),
            'schoolyear': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['CGL']
    symmetrical = True
