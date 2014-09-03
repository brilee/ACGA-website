import os
import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import Client
from django.contrib.auth import models as auth_models

from CGL.models import Season, Player, School, Membership, Round, Match, Game
from CGL.settings import current_seasons

from sgf import MySGFGame

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_SGF = os.path.join(CURR_DIR, 'test_files/testfile.sgf')

class TestWithCGLSetup(TestCase):
    def setUp(self):
        self.test_seasons = []
        for season in current_seasons:
            self.test_seasons.append(Season.objects.create(name=season))
        self.test_user = auth_models.User.objects.create(username='brilee')
        self.test_school = School.objects.create(name='test_school')
        self.test_player = Player.objects.create(name='test_player', school=self.test_school, pk=17)
        self.test_membership = Membership.objects.create(school=self.test_school, season=self.test_seasons[0])
        self.test_round = Round.objects.create(season=self.test_seasons[0], date=datetime.datetime.today())
        self.test_match = Match.objects.create(round=self.test_round, school1=self.test_school, school2=self.test_school)
        with open(TEST_SGF) as f:
            self.test_game = Game.objects.create(match=self.test_match, white_player=self.test_player, black_player=self.test_player, winning_school='School1', board=1, white_school='School1', gamefile=SimpleUploadedFile('testfile', f.read()))

    def tearDown(self):
        self.test_game.delete()

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
            '/CGL/schools/test_school/',
            '/CGL/results/',
            '/CGL/results/%s/' % self.test_seasons[0].slug_name,
            '/CGL/players/',
            '/CGL/players/%s/' % self.test_player.id,
            '/CGL/games/%s/' % self.test_game.id,
        ) 

        for url in urls:
            try:
                response = self.client.get(url)
                assert response.status_code == 200
            except:
                import traceback
                traceback.print_exc()
                print "Failed to get %s with response %s" % (url, response.status_code)

class ModelTests(TestWithCGLSetup):
    def test_game_properties(self):
        self.assertEquals(self.test_game.game_result, 'B+Resign')
        self.assertEquals(self.test_game.winner, self.test_game.black_player)
        self.assertEquals(self.test_game.loser, self.test_game.white_player)

class SGFParserTest(TestCase):
    def setUp(self):
        with open(TEST_SGF) as f:
            self.sgf_file = MySGFGame(f.read())

    def test_parse_result(self):
        self.assertEquals(self.sgf_file.game_result, 'B+Resign')
