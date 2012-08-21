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
    KGS_name = models.CharField(max_length=50, help_text="The prefix used for the KGS accounts")
    slug_name = models.SlugField(blank=True, editable=False)
    club_president = models.CharField(max_length=50, blank = True)
    captain = models.CharField(max_length=50)
    contact_email = models.EmailField()
    website = models.URLField(blank = True)
    meeting_info = models.TextField(blank=True)
#    managers = models.ForeignKey(SchoolUser)

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        super(School, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Player(models.Model):
    RANK_CHOICES = [(-9, '9d'), (-8, '8d'), (-7, '7d'), (-6, '6d'), (-5, '5d'), (-4, '4d'), (-3, '3d'), (-2, '2d'), (-1, '1d'), (1, '1k'), (2, '2k'), (3, '3k'), (4, '4k'), (5, '5k'), (6, '6k'), (7, '7k'), (8, '8k'), (9, '9k'), (10, '10k'), (11, '11k'), (12, '12k'), (13, '13k'), (14, '14k'), (15, '15k'), (16, '16k'), (17, '17k'), (18, '18k'), (19, '19k'), (20, '20k'), (21, '21k'), (22, '22k'), (23, '23k'), (24, '24k'), (25, '25k'), (26, '26k'), (27, '27k'), (28, '28k'), (29, '29k'), (30, '30k'), (100, '')]
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

    def browser_display_link(self):
        return unicode('/CGL/players/%s' % (self.slug_name))

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

class Membership(models.Model):
    school = models.ForeignKey(School)
    season = models.ForeignKey(Season)
    num_wins = models.IntegerField(editable=False, default = 0)
    num_losses = models.IntegerField(editable=False, default = 0)
    num_ties = models.IntegerField(editable=False, default = 0)

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
   
    class Meta:
        verbose_name_plural = 'Matches'
    
class Game(models.Model):
    def upload_location(instance, filename):
        return os.path.join(slugify(instance.match.round.season.name), slugify(instance.match.round.date), filename)

    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('School1', 'School1'), ('School2', 'School2'))
    
    match = models.ForeignKey(Match, help_text="This field determines who's 'School1' and who's 'School2'.")
    board = models.CharField(max_length = 1, choices = BOARD_CHOICES)
    gamefile = models.FileField(upload_to=upload_location)
    white_school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who played white? Hint: KGS filenames are formatted whitePlayer-blackPlayer")
    winner = models.CharField(max_length=10, choices=SCHOOL_CHOICES, help_text="Who won the game?")
    school1_player = models.ForeignKey(Player, related_name="game_school1_player")
    school2_player = models.ForeignKey(Player, related_name="game_school2_player")

    class Meta:
        ordering = ['-match__round__date', 'board']

    def browser_display_link(self):
        return unicode('/CGL/games/%s' % (self.id))
    
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

        if self.winner == 'School1':
            p1 = wrap_tag(p1, 'b')
        else:
            p2 = wrap_tag(p2, 'b')

        def add_player_link(arg):
            link = arg[1].browser_display_link()
            return wrap_tag(arg[0], 'a', extras='href="%s"' % link)

        (p1, p2) = map(add_player_link, ((p1, player1), (p2, player2)))

        sgf = wrap_tag('[sgf]', 'a', extras='href="%s"' % self.gamefile.url)
        game_link = wrap_tag('[view]', 'a', extras='href="%s"' % self.browser_display_link())
        
        almost_done = '%s %s Board %s: %s vs. %s' % (sgf, game_link, self.board, p1, p2)

        return unicode(wrap_tag(almost_done, 'li'))
        
        
##        contents = (self.board, self.browser_display_link(), self.school1_player.name, self.school1_player.get_rank_display(), self.school2_player.name, self.school2_player.get_rank_display())
##        before = '<li>Board %s: <a href="%s">'
##        after = '</a></li>'
##        if self.winner == 'School1':
##            if self.white_school == 'School1':
##                return unicode((before + '<b>%s, %s (W)</b> vs. %s, %s (B)' + after) % contents)
##            else:
##                return unicode((before + '<b>%s, %s (B)</b> vs. %s, %s (W)' + after) % contents)
##        else:
##            if self.white_school == 'School2':
##                return unicode((before + '%s, %s (W) vs. <b>%s, %s (B)</b>' + after) % contents)
##            else:
##                return unicode((before + '%s, %s (B) vs. <b>%s, %s (W)</b>' + after) % contents)

    def __unicode__(self):
        return unicode("%s vs. %s in %s vs. %s on %s, board %s" %(self.school1_player.name, self.school2_player.name, self.match.school1, self.match.school2, unicode(self.match.round.date), self.board))

class Forfeit(models.Model):
    BOARD_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))
    SCHOOL_CHOICES = (('School1', 'School1'), ('School2', 'School2'))

    match = models.ForeignKey(Match, help_text="School1 vs School2")
    board = models.CharField(max_length = 1, choices = BOARD_CHOICES)
    forfeit = models.CharField(max_length=10, choices = SCHOOL_CHOICES, help_text="Who forfeited the match?")

    class Meta:
        ordering = ['-match__round__date', 'board']

    def display_result(self):
        if self.forfeit == 'School1':
            return unicode('<li>Board %s: %s forfeits this board</li>' % (self.board, self.match.school1.name))
        else:
            return unicode('<li>Board %s: %s forfeits this board</li>' % (self.board, self.match.school2.name))

    def __unicode__(self):
        return unicode('%s vs %s on %s, board %s' %(self.match.school1, self.match.school2, self.match.round.date, self.board))

