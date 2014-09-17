import datetime
import os, shutil
from urllib import quote
from django.db import models
from django.db.models.signals import post_delete
from django.template.defaultfilters import slugify
from django.contrib.auth import models as auth_models
from django.dispatch.dispatcher import receiver

from django.conf import settings
from CGL.settings import current_ladder_season

from sgf import MySGFGame

SCHOOL1, SCHOOL2 = 'School1', 'School2'

def html_tag(tag):
    def f(text, **kwargs):
        '''
        Constructs an html tag. Assumes that text does not contain XSS attacks!
        Also assumes that text is already in bytes / encoded properly.
        '''
        if 'class_' in kwargs:
            class_value = kwargs.pop('class_')
            kwargs['class'] = class_value

        return "<{tag}{attrs}>{text}</{tag}>".format(
            tag=tag,
            attrs=''.join(' {item[0]}="{item[1]}"'.format(item=item) for item in sorted(kwargs.items())),
            text=text,
        )
    return f

a_tag = html_tag('a')
b_tag = html_tag('b')

class School(models.Model):
    name = models.CharField(max_length=50)
    KGS_name = models.CharField(blank=True, max_length=50, help_text="The prefix used for the KGS accounts")
    slug_name = models.SlugField(blank=True, editable=False)
    club_president = models.CharField(max_length=50, blank=True)
    captain = models.CharField(blank=True, max_length=50)
    contact_email = models.EmailField()
    website = models.URLField(blank=True)
    meeting_info = models.TextField(blank=True)
    active = models.BooleanField(default=True, help_text="Uncheck if school club appears to have died")
    inCGL = models.BooleanField(default=True, help_text="Uncheck if school is not participating in the CGL. Does not affect registration status, but only listing status on the CGL schools page.")

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
#        super(School, self).save(*args, **kwargs)
        if not self.pk:
            # just some utility things to initialize for new schools
            super(School, self).save(*args, **kwargs)
            p = Player(name="Unknown Player", school=self)
            p.save()
            from accounts.models import SchoolEditPermission
            perm = SchoolEditPermission(user=auth_models.User.objects.get(username='brilee'), school=self)
            perm.save()
        else:
            super(School, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_roster', [str(self.slug_name)]) 

    def __unicode__(self):
        return self.name

class Player(models.Model):
    RANK_CHOICES = ([(-10 * i, '%ip' % i) for i in range(9, 0, -1)] +
                    [(-1 * i, '%id' % i) for i in range(9, 0, -1)] +
                    [(i, '%ik' % i) for i in range(1,31)] +
                    [(100, '??')])
    name = models.CharField(max_length=30)
    slug_name = models.SlugField(blank=True, editable=False)
    rank = models.IntegerField(choices=RANK_CHOICES, default= 100)
    KGS_username = models.CharField(max_length=12, blank=True)
    school = models.ForeignKey(School)
    num_wins = models.IntegerField(editable=False, default=0)
    num_losses = models.IntegerField(editable=False, default=0)

    receiveSpam = models.BooleanField(default=True, help_text="Uncheck if player doesn't want to get email reminders")
    isActive = models.BooleanField(default=True, help_text="Uncheck if player is inactive. Do not delete player; the database keeps track of everybody's games, including inactive players")

    user = models.OneToOneField(auth_models.User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['school', 'name', 'rank']

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{} - {} {}".format(self.school.name, self.name, self.get_rank_display())

    def name_and_rank(self):
        return '{}, {}'.format(self.name.encode('utf8'), self.get_rank_display())

    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_player', [str(self.id)])

    def game_set(self):
        ''' Custom method because Game has two ForeignKeys to Player, so
        reverse lookup is not well-defined. This overloads to provide
        expected behavior '''
        games1 = self.white_player_game_set.all()
        games2 = self.black_player_game_set.all()
        all_games = games1 | games2
        all_games = all_games.order_by('-match__round__date')
        return all_games

class Season(models.Model):
    name = models.CharField(max_length=25, help_text="Season One, Season One Championship, etc.")
    slug_name = models.SlugField(blank=True, editable=False)
    schoolyear = models.CharField(max_length=40, help_text="2011-2012, etc.")
    schools = models.ManyToManyField(School, through='Membership')
    html = models.TextField(blank=True, help_text="Any custom HTML for this season you'd like to appear in the archives")
    description = models.TextField(blank=True, help_text="Any historical notes about this season you'd like to appear in the archives")

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Season, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
   
    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_seasons', [str(self.slug_name)])

class Membership(models.Model):
    school = models.ForeignKey(School)
    season = models.ForeignKey(Season)
    team_name = models.CharField(max_length=60, default='', blank=True, help_text="Leave this blank to default to name of school")
    num_wins = models.IntegerField(editable=False, default=0)
    num_losses = models.IntegerField(editable=False, default=0)
    num_ties = models.IntegerField(editable=False, default=0)
    num_byes = models.IntegerField(editable=False, default=0)
    num_forfeits = models.IntegerField(editable=False, default=0)
    still_participating = models.BooleanField(default=True, help_text="Uncheck this box if school has withdrawn from season. This will cause them to not be considered by the matching algorithm")

    class Meta:
        ordering = ['-season__pk', '-num_wins', 'num_losses', '-num_ties', 'num_forfeits']

    def __unicode__(self):
        return u"{} in {}".format(self.team_name, self.season.name)

    def save(self, *args, **kwargs):
        if self.team_name == '':
            self.team_name = self.school.name
        super(Membership, self).save(*args, **kwargs)

class RoundManager(models.Manager):
    # The season filter is implicit - generally you want to call these
    # as "season.round_set.get_next_round()"
    # A pity that django templates don't really curry correctly...
    def get_next_round(self):
        next_round = super(RoundManager, self
                        ).filter(date__gte=datetime.datetime.now()
                        ).order_by('date')
        if next_round:
            return next_round[0]
        else:
            return super(RoundManager,self).none()

    def get_previous_round(self):
        previous_round = self.get_recent_rounds(1)
        if previous_round:
            return previous_round[0]
        else:
            return super(RoundManager, self).none()
    
    def get_recent_rounds(self, depth):
        ''' depth is how many recent rounds you want to retrieve'''
        all_past_rounds = super(RoundManager, self
                        ).filter(date__lt=datetime.datetime.now()
                        ).order_by('-date')
        if len(all_past_rounds) < depth:
            return all_past_rounds
        else:
            return all_past_rounds[0:depth]

class Round(models.Model):
    season = models.ForeignKey(Season)
    date = models.DateField(help_text="YYYY-MM-DD")
    round_number = models.IntegerField(default=0, blank=True)
    objects = RoundManager()

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.round_number:
            previous_round_count = Round.objects.filter(date__lt=self.date, season=self.season).count()
            self.round_number = previous_round_count + 1
        super(Round, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '{} in {}'.format(unicode(self.date), self.season.name)
    
    def in_future(self):
        return self.date > datetime.date.today()

    def in_past(self):
        return self.date <= datetime.date.today()

    def in_near_future(self):
        return self.in_future() and self.date < datetime.date.today() + datetime.timedelta(days=14)

    def in_near_past(self):
        return self.in_past() and self.date > datetime.date.today() - datetime.timedelta(days=14)

class Bye(models.Model):
    school = models.ForeignKey(School)
    team = models.ForeignKey(Membership, null=True)
    round = models.ForeignKey(Round)

    class Meta:
        ordering = ['-round__date']

    def __unicode__(self):
        return u'{} got a bye on {}'.format(self.team.school.name, unicode(self.round.date))

class Match(models.Model):
    round = models.ForeignKey(Round)
    school1 = models.ForeignKey(School, related_name="school1")
    school2 = models.ForeignKey(School, related_name="school2")
    team1 = models.ForeignKey(Membership, related_name="team1", null=True)
    team2 = models.ForeignKey(Membership, related_name="team2", null=True)
    score1 = models.IntegerField(editable=False, default=0)
    score2 = models.IntegerField(editable=False, default=0)
    is_exhibition = models.BooleanField(default=False, help_text="This will cause match to not be considered in scoring")

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-round__date']
   
    def __unicode__(self):
        return u'{} vs. {} on {}'.format(self.team1.school.name, self.team2.school.name, unicode(self.round.date))

    def display_result(self):
        return (
            a_tag(self.team1.school.name.encode('utf8'), href=self.team1.school.get_absolute_url()) +
            ' ({} - {}) '.format(self.score1, self.score2) +
            a_tag(self.team2.school.name.encode('utf8'), href=self.team2.school.get_absolute_url()) +
            ' (Exhibition match)' if self.is_exhibition else ''
        )

    def display_match(self):
        return u"{} ({}) vs. {} ({})".format(self.team1.school.name,
                                             self.team1.school.KGS_name,
                                             self.team2.school.name,
                                             self.team2.school.KGS_name)

class GameBase(models.Model):
    gamefile = models.FileField(upload_to='temp_files', help_text="Please upload the SGF file. SGF files can be downloaded from KGS by right-clicking on the game record under a user's game list")
    white_player = models.ForeignKey(Player, related_name="white_player_%(class)s_set", null=True)
    black_player = models.ForeignKey(Player, related_name="black_player_%(class)s_set", null=True)
    game_result = models.CharField(max_length=10, editable=False, blank=True, default='')
    handicap = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # on first save, parse SGF file and extract result
            parsed_file = MySGFGame(self.gamefile.read())
            self.game_result = parsed_file.game_result
            self.handicap = parsed_file.handicap
        super(GameBase, self).save(*args, **kwargs)

    @property
    def first_display_player(self):
        '''Override this method in order to get customized result printouts'''
        return self.white_player

    @property
    def second_display_player(self):
        if self.first_display_player == self.black_player:
            return self.white_player
        else:
            return self.black_player

    def get_absolute_url(self):
        raise NotImplementedError()

    def download_html(self):
        return a_tag('[sgf]', href=self.gamefile.url)

    def view_html(self):
        return a_tag('[view]', href=self.get_absolute_url())

    def result_html(self):
        p1 = self.first_display_player
        p2 = self.second_display_player

        if self.first_display_player == self.white_player:
            c1, c2 = ' (W)', ' (B)'
        else:
            c1, c2 = ' (B)', ' (W)'

        if self.first_display_player == self.winner:
            n1 = b_tag(p1.name_and_rank() + c1)
            n2 = p2.name_and_rank() + c2
        else:
            n1 = p1.name_and_rank() + c1
            n2 = b_tag(p2.name_and_rank() + c2)

        return (
            a_tag(n1, href=p1.get_absolute_url()) +
            ' vs. ' +
            a_tag(n2, href=p2.get_absolute_url())
        )

    def full_description_html(self):
        return ' '.join((self.download_html(), self.view_html(), self.result_html()))

    @property
    def winner(self):
        if "b+" in self.game_result.lower():
            return self.black_player
        elif "w+" in self.game_result.lower():
            return self.white_player
        else:
                # ugh. Don't really want to deal with a Maybe type here so
            # I'm just going to default to letting W win.
            return self.white_player

    @property
    def loser(self):
        if self.winner == self.white_player:
            return self.black_player
        else:
            return self.white_player


class Game(GameBase):
    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = ((SCHOOL1, SCHOOL1), (SCHOOL2, SCHOOL2))
    
    match = models.ForeignKey(Match, help_text="This field determines who's 'School1' and who's 'School2'.")
    board = models.CharField(max_length=1, choices=BOARD_CHOICES)
    white_school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who played white? Hint: KGS filenames are usually formatted whitePlayer-blackPlayer")

    #obsolete
    winning_school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who won the game?", null=True)

    class Meta:
        ordering = ['-match__round__date', 'match__team1__school__name', 'board']

    def save(self, *args, **kwargs):
        # Implement custom upload_to behavior for filename
        temp_path = self.gamefile.name
        temp_dir, filename = os.path.split(temp_path)
        self.gamefile.storage.delete(temp_path)
        actual_path = os.path.join(slugify(self.match.round.season.name), slugify(self.match.round.date), filename)
        self.gamefile.storage.save(actual_path, self.gamefile)
        self.gamefile = actual_path
        super(Game, self).save(*args, **kwargs)

    @property
    def team1_player(self):
        if self.white_school == SCHOOL1:
            return self.white_player
        elif self.white_school == SCHOOL2:
            return self.black_player

    @property
    def team2_player(self):
        if self.white_school == SCHOOL2:
            return self.white_player
        elif self.white_school == SCHOOL1:
            return self.black_player

    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_game', [str(self.id)])

    def __unicode__(self):
        return u"{} vs. {} in {} vs. {} on {}, board {}".format(
            self.team1_player.name,
            self.team2_player.name,
            self.match.team1.school.name,
            self.match.team2.school.name,
            unicode(self.match.round.date),
            self.board
        )

class LadderGame(GameBase):
    season = models.ForeignKey(Season, blank=True, help_text="Leave this blank to default to current ladder season")

    def save(self, *args, **kwargs):
        if not self.season:
            self.season = Season.objects.get(name=current_ladder_season)
        # Implement custom upload_to behavior for filename
        temp_path = self.gamefile.name
        temp_dir, filename = os.path.split(temp_path)
        self.gamefile.storage.delete(temp_path)
        actual_path = os.path.join(slugify(self.season.name), 'ladder_games', filename)
        self.gamefile.storage.save(actual_path, self.gamefile)
        self.gamefile = actual_path
        super(LadderGame, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_ladder_game', [str(self.id)])

    def __unicode__(self):
        return u"{} vs {}".format(self.white_player.name, self.black_player.name)

class LadderMembership(models.Model):
    season = models.ForeignKey(Season)
    player = models.ForeignKey(Player)
    num_wins = models.IntegerField(editable=False, default=0)
    num_losses = models.IntegerField(editable=False, default=0)
    num_ties = models.IntegerField(editable=False, default=0)

    class Meta:
        ordering = ['-season__pk', '-num_wins', 'num_losses', '-num_ties']

    def __unicode__(self):
        return u"{} in {}".format(self.player.name, self.season.name)

@receiver(post_delete)
def delete_Game(sender, instance, **kwargs):
    if isinstance(instance, GameBase):
        subfolder, filename = os.path.split(instance.gamefile.name)
        instance.gamefile.delete(save=False)
        full_folder_path = os.path.join(settings.MEDIA_ROOT, subfolder)
        if not os.listdir(full_folder_path):
            shutil.rmtree(full_folder_path)

class Forfeit(models.Model):
    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('Team1', 'School1'), ('Team2', 'School2'))

    match = models.ForeignKey(Match, help_text="Team1 vs Team2")
    board = models.CharField(max_length=1, choices=BOARD_CHOICES)
    school1_noshow = models.BooleanField(default=False, blank=True, help_text="Did School 1 fail to show up?")
    school2_noshow = models.BooleanField(default=False, blank=True, help_text="Did School 2 fail to show up?")
    team1_noshow = models.BooleanField(default=False, blank=True, help_text="Did Team 1 fail to show up?")
    team2_noshow = models.BooleanField(default=False, blank=True, help_text="Did Team 2 fail to show up?")

    class Meta:
        ordering = ['-match__round__date', 'board']

    def display_result(self):
        if self.team1_noshow and self.team2_noshow:
            return 'Board %s: Both schools failed to show' % self.board
        elif self.team1_noshow and not self.team2_noshow:
            return 'Board %s: %s forfeits this board' % (self.board, self.match.team1.school.name.encode('utf8'))
        elif not self.team1_noshow and self.team2_noshow:
            return 'Board %s: %s forfeits this board' % (self.board, self.match.team2.school.name.encode('utf8'))
        else:
            return 'Board %s: Invalid forfeit record, at least one school must be marked as noshow' % self.board

    def __unicode__(self):
        return u'{} vs {} on {}, board {}'.format(self.match.team1.school.name, self.match.team2.school.name, unicode(self.match.round.date), self.board)

class CommentBase(models.Model):
    user = models.ForeignKey(auth_models.User)
    datetime = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=1000)

    class Meta:
        abstract = True
        ordering = ['-datetime']

    def __unicode__(self):
        return u'{}: {}'.format(self.user.username, self.comment[:100])

class GameComment(CommentBase):
    game = models.ForeignKey(Game)

class LadderGameComment(CommentBase):
    game = models.ForeignKey(LadderGame)
