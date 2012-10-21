from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.db.models import Count
from django.contrib.auth import models as auth_models
from settings import current_season_name
import datetime
import os

def wrap_tag(text, tag, extras=False):
    '''
    Wraps an html tag around some text.
    Tag should be specified without brackets.
    Extras should be given as raw text - 'id="someID"'
    '''
    if extras:
        open_tag = '<' + tag + ' ' + extras + '>'
    else:
        open_tag = '<' + tag + '>'
    close_tag = '</' + tag + '>'

    return open_tag + text + close_tag

#class SchoolUser(models.Model):
#    user = models.ForeignKey(auth_models.User, unique=True)

class School(models.Model):
    name = models.CharField(max_length=50)
    KGS_name = models.CharField(blank=True, max_length=50, help_text="The prefix used for the KGS accounts")
    slug_name = models.SlugField(blank=True, editable=False)
    club_president = models.CharField(max_length=50, blank = True)
    captain = models.CharField(blank=True, max_length=50)
    contact_email = models.EmailField()
    website = models.URLField(blank = True)
    meeting_info = models.TextField(blank=True)
    inCGL = models.BooleanField(default=True, help_text="Uncheck if school is not participating in the CGL.")

#    managers = models.ForeignKey(SchoolUser)

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(School, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('CGA.CGL.views.display_roster', [str(self.slug_name)]) 

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Player(models.Model):
    RANK_CHOICES = ([(-10 * i, '%ip' % i) for i in range(9, 0, -1)] +
                    [(-1 * i, '%id' % i) for i in range(9, 0, -1)] +
                    [(i, '%ik' % i) for i in range(1,31)] +
                    [(100, '??')])
    name = models.CharField(max_length=30)
    slug_name = models.SlugField(blank=True, editable=False)
    rank = models.IntegerField(choices = RANK_CHOICES, blank=True, default= 100)
    KGS_username = models.CharField(max_length=12, blank=True)
    school = models.ForeignKey(School)
    num_wins = models.IntegerField(editable=False, default = 0)
    num_losses = models.IntegerField(editable=False, default = 0)
    
    isActive = models.BooleanField(default=True, help_text="Uncheck if player is inactive. Do not delete player; the database keeps track of everybody's games, including inactive players")

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode("%s - %s" %(self.school.name, self.name))

    def name_and_rank(self):
        return unicode('%s, %s' % (self.name, self.get_rank_display()))

    @models.permalink
    def get_absolute_url(self):
        return ('CGA.CGL.views.display_player', [str(self.id)])

    def game_set(self):
        ''' Custom method because Game has two ForeignKeys to Player, so
        reverse lookup is not well-defined. This overloads to provide
        expected behavior '''
        games1 = self.game_school1_player.all()
        games2 = self.game_school2_player.all()
        all_games = games1 | games2
        all_games = all_games.order_by('-match__round__date')
        return all_games
    
    class Meta:
        ordering = ['school', 'name', 'rank']

class Season(models.Model):
    name = models.CharField(max_length = 25, help_text="Season One, Season One Championship, etc.")
    slug_name = models.SlugField(blank=True, editable=False)
    schoolyear = models.CharField(max_length = 40, help_text="2011-2012, etc.")
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
        return ('CGA.CGL.views.display_season', [str(self.slug_name)])


class Membership(models.Model):
    school = models.ForeignKey(School)
    season = models.ForeignKey(Season)
    num_wins = models.IntegerField(editable=False, default = 0)
    num_losses = models.IntegerField(editable=False, default = 0)
    num_ties = models.IntegerField(editable=False, default = 0)
    num_forfeits = models.IntegerField(editable=False, default = 0)

    def __unicode__(self):
        return unicode("%s in %s" %(self.school, self.season))

class RoundManager(models.Manager):
    current_season = Season.objects.get(name=current_season_name)
    def get_next_round(self):
        next_round = super(RoundManager, self
                     ).filter(season=self.current_season
                        ).filter(date__gte=datetime.datetime.now()
                        ).order_by('date')
        if next_round:
            return next_round[0]
        else:
            return super(RoundManager,self).none()

    def get_previous_round(self):
        return self.get_recent_rounds(1)[0]
    
    def get_recent_rounds(self, depth):
        ''' depth is how many recent rounds you want to retrieve'''
        all_past_rounds = super(RoundManager, self
                     ).filter(season=self.current_season
                        ).filter(date__lt=datetime.datetime.now()
                        ).order_by('-date')
        if len(all_past_rounds) < depth:
            return all_past_rounds
        else:
            return all_past_rounds[0:depth]

class Round(models.Model):
    season = models.ForeignKey(Season)
    date = models.DateField(help_text="YYYY-MM-DD")
    objects = RoundManager()

    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return unicode(self.date)

class Match(models.Model):
    round = models.ForeignKey(Round)
    school1 = models.ForeignKey(School, related_name="school1")
    school2 = models.ForeignKey(School, related_name="school2")
    score1 = models.IntegerField(editable=False, default=0)
    score2 = models.IntegerField(editable=False, default=0)

   
    def __unicode__(self):
        return unicode("%s vs. %s on %s" %(self.school1.name, self.school2.name,unicode(self.round.date)))

    def display_result(self):
        if self.score1 > self.score2:
            return unicode('%s defeats %s, %s - %s' %(self.school1.name,
                                                       self.school2.name,
                                                       self.score1,
                                                       self.score2))
        elif self.score2 > self.score1:
            return unicode('%s defeats %s, %s - %s' %(self.school2.name,
                                                       self.school1.name,
                                                       self.score2,
                                                       self.score1))
        else:
            return unicode('%s ties  %s, %s - %s' %(self.school1.name,
                                                    self.school2.name,
                                                    self.score1,
                                                    self.score2))
    
    class Meta:
        verbose_name_plural = 'Matches'
        ordering = ['-round__date']

class Game(models.Model):
    def upload_location(instance, filename):
        return os.path.join(slugify(instance.match.round.season.name), slugify(instance.match.round.date), filename)

    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('School1', 'School1'), ('School2', 'School2'))
    
    match = models.ForeignKey(Match, help_text="This field determines who's 'School1' and who's 'School2'.")
    board = models.CharField(max_length = 1, choices = BOARD_CHOICES)
    gamefile = models.FileField(upload_to=upload_location)
    white_school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who played white? Hint: KGS filenames are formatted whitePlayer-blackPlayer")
    winning_school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who won the game?")
    school1_player = models.ForeignKey(Player, related_name="game_school1_player")
    school2_player = models.ForeignKey(Player, related_name="game_school2_player")

    class Meta:
        ordering = ['-match__round__date', 'board']

    def white_player(self):
        if self.white_school == 'School1':
            return self.school1_player
        else:
            return self.school2_player

    def black_player(self):
        if self.white_school == 'School1':
            return self.school2_player
        else:
            return self.school1_player
       
    def winner(self):
        if self.winning_school == 'School1':
            return self.school1_player
        else:
            return self.school2_player
    
    @models.permalink
    def get_absolute_url(self):
        return ('CGA.CGL.views.display_game', [str(self.id)])
    
    def display_result(self):
        '''
        Generates a nice representation of the game, with the format:
        School_1 player vs. School_2 player [sgf link]
        with the winner's name in bold.
        '''
        player1 = self.school1_player
        player2 = self.school2_player
        
        p1 = player1.name_and_rank()
        p2 = player2.name_and_rank()
        
        if self.white_school == 'School1':
            p1 += ' (W)'
            p2 += ' (B)'
        else:
            p2 += ' (W)'
            p1 += ' (B)'

        if self.winning_school == 'School1':
            p1 = wrap_tag(p1, 'b')
        else:
            p2 = wrap_tag(p2, 'b')

        def add_player_link(arg):
            link = arg[1].get_absolute_url()
            return wrap_tag(arg[0], 'a', extras='href="%s"' % link)

        (p1, p2) = map(add_player_link, ((p1, player1), (p2, player2)))

        sgf = wrap_tag('[sgf]', 'a', extras='href="%s"' % self.gamefile.url)
        game_link = wrap_tag('[view]', 'a', extras='href="%s"' % self.get_absolute_url())
        
        almost_done = '%s %s Board %s: %s vs. %s' % (sgf, game_link, self.board, p1, p2)

        return unicode(wrap_tag(almost_done, 'li'))

    def __unicode__(self):
        return unicode("%s vs. %s in %s vs. %s on %s, board %s" %(self.school1_player.name, self.school2_player.name, self.match.school1, self.match.school2, unicode(self.match.round.date), self.board))

class Forfeit(models.Model):
    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('School1', 'School1'), ('School2', 'School2'))

    match = models.ForeignKey(Match, help_text="School1 vs School2")
    board = models.CharField(max_length = 1, choices = BOARD_CHOICES)
    school1_noshow = models.BooleanField(default=False, blank=True, help_text="Did School 1 fail to show up?")
    school2_noshow = models.BooleanField(default=False, blank=True, help_text="Did School 2 fail to show up?")

    class Meta:
        ordering = ['-match__round__date', 'board']

    def display_result(self):
        if self.school1_noshow and self.school2_noshow:
            return unicode('<li>Board %s: Both schools failed to show</li>' % self.board)
        elif self.school1_noshow and not self.school2_noshow:
            return unicode('<li>Board %s: %s forfeits this board</li>' % (self.board, self.match.school1.name))
        elif not self.school1_noshow and self.school2_noshow:
            return unicode('<li>Board %s: %s forfeits this board</li>' % (self.board, self.match.school2.name))

    def __unicode__(self):
        return unicode('%s vs %s on %s, board %s' %(self.match.school1, self.match.school2, self.match.round.date, self.board))

