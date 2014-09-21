from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from CGL.models import * 

class PlayerProfileInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'profile'

class PlayerAdmin(UserAdmin):
    inlines = (PlayerProfileInline, )

class GameAdmin(admin.ModelAdmin):
    fields = ('match', 'gamefile', 'white_school', 'white_player', 'black_player', 'board')

admin.site.register(School)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(Membership)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(Game, GameAdmin)
admin.site.register(LadderGame)
admin.site.register(Bye)
admin.site.register(Forfeit)
admin.site.register(GameComment)
admin.site.register(LadderGameComment)
admin.site.unregister(User)
admin.site.register(User, PlayerAdmin)


