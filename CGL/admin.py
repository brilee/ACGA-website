from django import forms
from django.contrib import admin
from singleton_models.admin import SingletonModelAdmin
from CGL.models import * 

class PlayerProfileInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'profile'

class GameAdmin(admin.ModelAdmin):
    fields = ('match', 'gamefile', 'white_school', 'white_player', 'black_player', 'board')

class TeamAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # hack to get the actual instance being referred to by the admin view.
        team_id = filter(bool, request.path.split('/'))[-1]
        team = Team.objects.get(id=team_id)
        if db_field.name == "players":
             kwargs["queryset"] = Player.objects.filter(school=team.school)
        return super(TeamAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(School)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(CurrentSeasons, SingletonModelAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(Game, GameAdmin)
admin.site.register(Bye)
admin.site.register(Forfeit)
admin.site.register(SchoolAuth)
