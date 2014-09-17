# -*- coding: utf-8 -*-
import os
import datetime

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.contrib.auth import models as auth_models

from accounts.models import SchoolEditPermission
from CGL.models import Season, Player, School, Membership, Round, Match, Game, Forfeit, LadderGame, GameComment, LadderGameComment, a_tag
from CGL.views import submit_comment, submit_ladder_comment
from CGL.settings import current_seasons

from sgf import MySGFGame

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_SGF = os.path.join(CURR_DIR, 'test_files/testfile.sgf')
TEST_SGF2 = os.path.join(CURR_DIR, 'test_files/testfile2.sgf')

class TestWithCGLSetup(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='tester', email="tester@test.com", password='omgsuchsecret')
        self.client.login(username='tester', password='omgsuchsecret')

        auth_models.User.objects.create(username=u'brilee')
        self.test_seasons = []
        for season in current_seasons:
            self.test_seasons.append(Season.objects.create(name=season))
        self.test_school = School.objects.create(name=u'Test School')
        self.test_school2 = School.objects.create(name=u'Test School 2')
        self.test_player = Player.objects.create(name=u'☃player', school=self.test_school, pk=17, rank=-2)
        self.test_membership = Membership.objects.create(school=self.test_school, season=self.test_seasons[0])
        self.test_round = Round.objects.create(season=self.test_seasons[0], date=datetime.datetime.today())
        self.test_match = Match.objects.create(round=self.test_round, team1=self.test_membership, team2=self.test_membership, school1=self.test_school, school2=self.test_school)
        self.test_forfeit = Forfeit.objects.create(match=self.test_match, board=1, school1_noshow=True)

        with open(TEST_SGF) as f:
            sgf_contents = f.read()

        self.test_game = Game.objects.create(match=self.test_match, white_player=self.test_player, black_player=self.test_player, board=1, white_school='School1', gamefile=SimpleUploadedFile('testfile', sgf_contents))
        self.test_ladder_game = LadderGame.objects.create(season=self.test_seasons[0], white_player=self.test_player, black_player=self.test_player, gamefile=SimpleUploadedFile('testfile', sgf_contents))

        self.test_permission = SchoolEditPermission.objects.create(school=self.test_school, user=self.test_user)

    def tearDown(self):
        self.test_game.delete()
        self.test_ladder_game.delete()

class IntegrationTest(TestWithCGLSetup):
    def test_all_views(self):
        # NB: all urls must have trailing slash, or else will trigger 301 redirects to slash version, breaking the test... :(
        urls = (
            '/',
            '/home/',
            '/resources/',
            '/ing/',
            '/about/',
            '/members/',
            '/allemail/',
            '/events/',
            '/CGL/',
            '/CGL/rules/',
            '/CGL/schools/',
            '/CGL/schools/%s/' % self.test_school.slug_name,
            '/CGL/results/',
            '/CGL/results/%s/' % self.test_seasons[0].slug_name,
            '/CGL/players/',
            '/CGL/players/%s/' % self.test_player.id,
            '/CGL/games/%s/' % self.test_game.id,
            '/CGL/laddergames/%s/' % self.test_ladder_game.id,
        ) 

        for url in urls:
            try:
                response = self.client.get(url)
                assert response.status_code == 200
            except:
                import traceback
                traceback.print_exc()
                print "Failed to get %s with response %s" % (url, response.status_code)

    def test_public_post_views(self):
        url_comment = (
            ('/CGL/games/%s/submit/' % self.test_game.id, GameComment),
            ('/CGL/laddergames/%s/submit/' % self.test_ladder_game.id, LadderGameComment)
        )
        for url, comment_model in url_comment:
            comment_text = 'Test Comment to %s' % url
            try:
                response = self.client.post(url, {'comment': comment_text})
            except:
                import traceback
                traceback.print_exc()
            self.assertEquals(response.status_code, 302)
            new_comment = comment_model.objects.get(pk=1)
            self.assertEquals(new_comment.comment, comment_text)

#    def test_captain_edit_views(self):


class ModelTests(TestWithCGLSetup):
    def test_round_autoassign(self):
        self.assertEquals(self.test_round.round_number, 1)
    def test_html_tags(self):
        self.assertEquals(
            a_tag('Click Here!', href='blah.com', class_='hello there'),
            '<a class="hello there" href="blah.com">Click Here!</a>'
        )
        self.assertEquals(
            a_tag('No attrs here'),
            '<a>No attrs here</a>'
        )

    def test_game_display(self):
        self.assertEquals(
            self.test_game.result_html(),
            '<a href="/CGL/players/17/"><b>\xe2\x98\x83player, 2d (W)</b></a> vs. <a href="/CGL/players/17/">\xe2\x98\x83player, 2d (B)</a>'
        )
        self.assertEquals(
            self.test_game.view_html(),
            '<a href="/CGL/games/1/">[view]</a>'
        )
        self.assertEquals(
            self.test_game.download_html(),
            '<a href="{}">[sgf]</a>'.format(self.test_game.gamefile.url)
        )

    def test_edit_permissions(self):
        self.assertTrue(SchoolEditPermission.objects.has_edit_permissions(self.test_user, self.test_school))
        self.assertTrue(SchoolEditPermission.objects.has_edit_permissions(self.test_user, self.test_player))
        self.assertTrue(SchoolEditPermission.objects.has_edit_permissions(self.test_user, self.test_game))
        self.assertTrue(SchoolEditPermission.objects.has_edit_permissions(self.test_user, self.test_forfeit))
        self.assertTrue(not SchoolEditPermission.objects.has_edit_permissions(self.test_user, self.test_school2))

    def test_membership_autofill(self):
        self.assertEquals(self.test_membership.team_name, self.test_membership.school.name)

    def test_game_properties(self):
        self.assertEquals(self.test_game.game_result, 'B+Resign')
        self.assertEquals(self.test_game.winner, self.test_game.black_player)
        self.assertEquals(self.test_game.loser, self.test_game.white_player)

class SGFParserTest(TestCase):
    def test_parse_result(self):
        with open(TEST_SGF) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.game_result, 'B+Resign')
        with open(TEST_SGF2) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.game_result, 'W+9.50')

    def test_parse_handicap(self):
        with open(TEST_SGF) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.handicap, 0)

        with open(TEST_SGF2) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.handicap, 4)
