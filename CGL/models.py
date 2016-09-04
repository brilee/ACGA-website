import datetime
import os, shutil
import random
import string
from django.db import models
from django.db.models.signals import post_delete
from django.template.defaultfilters import slugify
from django.contrib.auth import models as auth_models
from django.dispatch.dispatcher import receiver

from django.conf import settings

from singleton_models.models import SingletonModel

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
    KGS_password = models.CharField(blank=True, max_length=50, help_text="password base used for KGS accounts")
    slug_name = models.SlugField(blank=True, editable=False)
    club_president = models.CharField(max_length=50, blank=True)
    captain = models.CharField(blank=True, max_length=50)
    contact_email = models.EmailField()
    secondary_contacts = models.CharField(blank=True, max_length=100, help_text="Comma separated list of alternate emails to be cc'd on communications")
    website = models.URLField(blank=True)
    meeting_info = models.TextField(blank=True)
    active = models.BooleanField(default=True, help_text="Uncheck if school club appears to have died")
    inCGL = models.BooleanField(default=True, editable=False)

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
            SchoolAuth.objects.get_or_create(school=self)
        else:
            super(School, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('CGL.views.display_roster', [str(self.slug_name)]) 

    def __unicode__(self):
        return self.name

    def all_contact_emails(self):
        if self.secondary_contacts:
            return [self.contact_email] + self.secondary_contacts.split(',')
        else:
            return [self.contact_email]


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
        return u"{} {} - {}".format(self.name, self.get_rank_display(), self.school.name)

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
    is_championship = models.BooleanField(default=False)
    schools = models.ManyToManyField(School, through='Team')
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

    def get_captain_edit_url(self):
        return ('CGL.views.edit_season_matches', [str(self.slug_name)])

class CurrentSeasonsManager(models.Manager):
    def get(self):
        curr_seasons_singleton = self.all()
        if not curr_seasons_singleton:
            c = CurrentSeasons()
            c.save()
        else:
            c = curr_seasons_singleton[0]
        return c.current_seasons.all()

class CurrentSeasons(SingletonModel):
    current_seasons = models.ManyToManyField(Season)
    objects = CurrentSeasonsManager()

    def __unicode__(self):
        return u'Current seasons'

    class Meta:
        verbose_name = "Current seasons"
        verbose_name_plural = "Current seasons"

class Team(models.Model):
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
        return u"{} in {}{}".format(
            self.team_name,
            self.season.name,
            ' (Inactive)' if not self.still_participating else ''
        )

    def save(self, *args, **kwargs):
        if self.team_name == '':
            self.team_name = self.school.name
        super(Team, self).save(*args, **kwargs)

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

class Match(models.Model):
    round = models.ForeignKey(Round)
    team1 = models.ForeignKey(Team, related_name="team1", null=True)
    team2 = models.ForeignKey(Team, related_name="team2", null=True)
    score1 = models.IntegerField(editable=False, default=0)
    score2 = models.IntegerField(editable=False, default=0)
    is_exhibition = models.BooleanField(default=False, help_text="This will cause match to not be considered in scoring")

    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-round__date']
   
    def __unicode__(self):
        return u'{} vs. {} on {}'.format(self.team1.team_name, self.team2.team_name, unicode(self.round.date))

    def display_result(self):
        return '{} ({} - {}) {}'.format(self.team1.team_name.encode('utf8'), self.score1, self.score2, self.team2.team_name.encode('utf8'))

    def display_result_html(self):
        return (
            a_tag(self.team1.team_name.encode('utf8'), href=self.team1.school.get_absolute_url()) +
            ' ({} - {}) '.format(self.score1, self.score2) +
            a_tag(self.team2.team_name.encode('utf8'), href=self.team2.school.get_absolute_url()) +
            (' (Exhibition match)' if self.is_exhibition else '')
        )

    def display_match(self):
        return u"{} ({}) vs. {} ({})".format(self.team1.team_name,
                                             self.team1.school.KGS_name,
                                             self.team2.team_name,
                                             self.team2.school.KGS_name)

class GameBase(models.Model):
    def upload_to(instance, filename):
        if instance.__class__.__name__ == 'Game':
            return os.path.join(slugify(instance.match.round.season.name), slugify(instance.match.round.date), filename)
        else:
            return 'temp'

    gamefile = models.FileField(upload_to=upload_to, help_text="Please upload the SGF file. SGF files can be downloaded from KGS by right-clicking on the game record under a user's game list")
    white_player = models.ForeignKey(Player, related_name="white_player_%(class)s_set", null=True)
    black_player = models.ForeignKey(Player, related_name="black_player_%(class)s_set", null=True)
    game_result = models.CharField(max_length=10, editable=False, blank=True, default='')
    handicap = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            # on first save, parse SGF file and extract result
            self.gamefile.seek(0)
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

    class Meta:
        ordering = ['-match__round__date', 'match__team1__school__name', 'board']

    @property
    def team1_player(self):
        if self.white_school == SCHOOL1:
            return self.white_player
        elif self.white_school == SCHOOL2:
            return self.black_player

    @team1_player.setter
    def team1_player(self, val):
        if self.white_school == SCHOOL1:
            self.white_player = val
        elif self.white_school == SCHOOL2:
            self.black_player = val

    @property
    def team2_player(self):
        if self.white_school == SCHOOL2:
            return self.white_player
        elif self.white_school == SCHOOL1:
            return self.black_player

    @team2_player.setter
    def team2_player(self, val):
        if self.white_school == SCHOOL2:
            self.white_player = val
        elif self.white_school == SCHOOL1:
            self.black_player = val

    @property
    def first_display_player(self):
        return self.team1_player

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

@receiver(post_delete)
def delete_Game(sender, instance, **kwargs):
    if isinstance(instance, GameBase):
        subfolder, filename = os.path.split(instance.gamefile.name)
        instance.gamefile.delete(save=False)
        full_folder_path = os.path.join(settings.MEDIA_ROOT, subfolder)
        try:
            if not os.listdir(full_folder_path):
                shutil.rmtree(full_folder_path)
        except: pass

class Forfeit(models.Model):
    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('Team1', 'School1'), ('Team2', 'School2'))

    match = models.ForeignKey(Match, help_text="Team1 vs Team2")
    board = models.CharField(max_length=1, choices=BOARD_CHOICES)
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

class Bye(models.Model):
    team = models.ForeignKey(Team, null=True)
    round = models.ForeignKey(Round)

    class Meta:
        ordering = ['-round__date']

    def __unicode__(self):
        return u'{} got a bye on {}'.format(self.team.school.name, unicode(self.round.date))

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

class SchoolAuth(models.Model):
    school = models.ForeignKey(School)
    secret_key = models.CharField(max_length=16, null=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        super(SchoolAuth, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}: captain_school_auth={}'.format(self.school, self.secret_key)