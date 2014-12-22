# -*- coding: utf-8 -*-
import os
import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth import models as auth_models
from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory

from accounts.models import SchoolEditPermission
from CGL.models import Season, Player, School, Membership, Round, Match, Game, Forfeit, Bye, LadderGame, GameComment, LadderGameComment, a_tag
from CGL.views import submit_comment, submit_ladder_comment
from CGL.settings import current_seasons
from CGL.matchmaking import construct_matrix, score_matchups, make_random_matchup, best_matchup

from sgf import MySGFGame

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_SGF = os.path.join(CURR_DIR, 'test_files/testfile.sgf')
TEST_SGF2 = os.path.join(CURR_DIR, 'test_files/testfile2.sgf')
TEST_SGF3 = os.path.join(CURR_DIR, 'test_files/testfile3.sgf')

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
        self.test_match = Match.objects.create(round=self.test_round, team1=self.test_membership, team2=self.test_membership)
        self.test_forfeit = Forfeit.objects.create(match=self.test_match, board=1, team1_noshow=True)

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
                self.assertEquals(response.status_code, 302)
                new_comment = comment_model.objects.get(pk=1)
                self.assertEquals(new_comment.comment, comment_text)
            except:
                import traceback
                traceback.print_exc()

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
        # with open(TEST_SGF3) as f:
        #     sgf_file = MySGFGame(f.read())
        # self.assertEquals(sgf_file.game_result, 'B+59.50')

    def test_parse_handicap(self):
        with open(TEST_SGF) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.handicap, 0)

        with open(TEST_SGF2) as f:
            sgf_file = MySGFGame(f.read())
        self.assertEquals(sgf_file.handicap, 4)

class MatchmakingTest(TestCase):
    def setUp(self):
        auth_models.User.objects.create(username=u'brilee')
        self.test_season = Season.objects.create(name='Season Blah')
        self.round1 = Round.objects.create(season=self.test_season, date=datetime.datetime.today(), round_number=1)
        self.round2 = Round.objects.create(season=self.test_season, date=datetime.datetime.today(), round_number=2)
        self.schools = [School.objects.create(id=i, name=str(i)) for i in range(7)]
        self.teams = [Membership.objects.create(school=s, season=self.test_season, id=s.id) for s in self.schools]

        # Records so far
        # Sc W L T B F
        WLTBF = (
            (3, 0, 0, 0, 0),
            (2, 0, 0, 1, 3),
            (2, 1, 0, 0, 1),
            (1, 1, 1, 1, 3),
            (0, 2, 0, 1, 4),
            (0, 2, 0, 1, 0),
            (0, 3, 0, 0, 8),
        )
        self.matches = [
            Match.objects.create(round=self.round1, team1=self.teams[0], team2=self.teams[1], score1=3, score2=2),
            Match.objects.create(round=self.round1, team1=self.teams[2], team2=self.teams[3], score1=3, score2=2),
            Match.objects.create(round=self.round1, team1=self.teams[5], team2=self.teams[6], score1=3, score2=2),
        ]
        for team, (win, loss, tie, bye, forfeit) in zip(self.teams, WLTBF):
            team.num_wins = win
            team.num_losses = loss
            team.num_ties = tie
            team.num_byes = bye
            team.num_forfeits = forfeit
            team.save()

        self.expected_pairings = [
            (self.teams[0], self.teams[2]),
            (self.teams[1], self.teams[3]),
            (self.teams[4], self.teams[5]),
        ]
        self.expected_bye = self.teams[6]


    def test_construct_matrix(self):
        matrix = construct_matrix(self.matches)
        # print '\n'.join("%s %s %s %s" % (i, j, matrix[i][j], matrix[j][i]) for i in range(7) for j in range(7) if i!=j)
        self.assertTrue(matrix[0][1])
        self.assertTrue(matrix[1][0])
        self.assertTrue(matrix[2][3])
        self.assertTrue(not matrix[2][4])
        self.assertTrue(not matrix[2][1000])

    def test_score_matchups(self):
        matrix = construct_matrix(self.matches)
        pairings = [
            (self.teams[0], self.teams[2]),
            (self.teams[1], self.teams[3]),
            (self.teams[4], self.teams[5]),
        ]
        self.assertEquals(
            score_matchups(pairings, self.teams[4], matrix),
            310
        )

    def test_make_random_matchup(self):
        pairings, bye = make_random_matchup(self.teams)
        self.assertEquals(len(pairings), 3)
        self.assertTrue(bool(bye))

    def test_best_matchup(self):
        success = 0
        total = 0
        for i in range(10):
            pairings, bye = best_matchup(self.teams, self.matches)
            if all(p==ep for p, ep in zip(pairings, self.expected_pairings)) and self.expected_bye == bye:
                success +=1
            total +=1
        self.assertEquals(success, total)

    def test_call_command(self):
        call_command('round_pairings', season=self.test_season.name, round='2')
        byes = Bye.objects.filter(round=self.round2)
        self.assertEquals(len(byes), 1)
        self.assertEquals(byes[0].team, self.expected_bye)

        matches = self.round2.match_set.all()
        self.assertEquals(len(matches), 3)
        sorted_matches = sorted(matches, key=lambda m: m.team1.id)
        for match, pairing in zip(sorted_matches, self.expected_pairings):
            self.assertEquals(match.team1, pairing[0])
            self.assertEquals(match.team2, pairing[1])

class ScoreUpdaterTest(TestCase):
    def setUp(self):
        auth_models.User.objects.create(username=u'brilee')

        self.test_season = Season.objects.create(name='Season Four')
        self.schools = [School.objects.create(id=i, name=str(i)) for i in range(4)]
        self.teams = [Membership.objects.create(school=s, season=self.test_season, id=s.id) for s in self.schools]

        self.players = [
            [Player.objects.create(name=u'school%splayer%s' % (j, i), school=self.schools[j]) for i in range(3)] 
            for j in range(4)
        ]

        self.rounds = [
            Round.objects.create(season=self.test_season, date=datetime.datetime.today(), round_number=0),
            Round.objects.create(season=self.test_season, date=datetime.datetime.today(), round_number=1),
        ]

        round_pairings = (
            ((0, 1), (2, 3)),
            ((0, 2), (1, 3)),
        )

        self.matches = [
            [
                Match.objects.create(round=self.rounds[round_no], team1=self.teams[pairing[0]], team2=self.teams[pairing[1]])
                for pairing in round
            ] for round_no, round in enumerate(round_pairings)
        ]

        with open(TEST_SGF) as f:
            # this sgf has B+resign.
            sgf_contents = f.read()

        for round in self.rounds:
            for match in round.match_set.all():
                Game.objects.create(
                    match=match,
                    white_player=self.players[match.team1.id][1],
                    black_player=self.players[match.team2.id][1],
                    board=1,
                    white_school='School1',
                    gamefile=SimpleUploadedFile('testfile', sgf_contents),
                )
                Game.objects.create(
                    match=match,
                    white_player=self.players[match.team2.id][2],
                    black_player=self.players[match.team1.id][2],
                    board=2,
                    white_school='School2',
                    gamefile=SimpleUploadedFile('testfile', sgf_contents),
                )
                Forfeit.objects.create(match=match, board=3, team1_noshow=True)

        Bye.objects.create(
            team=self.teams[0],
            round=self.rounds[0],
        )

    def tearDown(self):
        for g in Game.objects.all():
            g.delete()

    def testUpdateScores(self):
        call_command('update_scores', self.test_season.name)

        expected_player_results = [
            (0, 0),
            (0, 0),
            (0, 2),
            (2, 0),
            (0, 0),
            (1, 1),
            (1, 1),
            (0, 0),
            (1, 1),
            (1, 1),
            (0, 0),
            (2, 0),
        ]

        expected_match_results = [
            (1, 2),
            (1, 2),
            (1, 2),
            (1, 2),            
        ]

        expected_team_results = [
            (0, 2, 2),
            (1, 1, 1),
            (1, 1, 1),
            (2, 0, 0),
        ]

        for p_id, (wins, losses) in zip(range(1, 13), expected_player_results):
            player = Player.objects.get(id=p_id)
            self.assertEquals(wins, player.num_wins)
            self.assertEquals(losses, player.num_losses)
        for m_id, (team1score, team2score) in zip(range(1, 5), expected_match_results):
            match = Match.objects.get(id=m_id)
            self.assertEquals(team1score, match.score1)
            self.assertEquals(team2score, match.score2)
        for t_id, (wins, losses, forfeits) in enumerate(expected_team_results):
            team = Membership.objects.get(id=t_id)
            self.assertEquals(wins, team.num_wins)
            self.assertEquals(losses, team.num_losses)
            self.assertEquals(forfeits, team.num_forfeits)

        self.assertEquals(Membership.objects.get(id=0).num_byes, 1)

