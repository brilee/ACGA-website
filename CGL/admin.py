from django.contrib import admin
from CGA.CGL.models import * 
from guardian.admin import GuardedModelAdmin

class SchoolAdmin (GuardedModelAdmin):
#    def queryset(self, request):
#        qs = super(GuardedModelAdmin, self).queryset(request)
#
#        if request.user.is_superuser:
#            return qs
#
#        user_qs = SchoolUser.objects.filter(user=request.user)
#        return qs.filter(managers__in=user_qs)
    pass
class PlayerAdmin (GuardedModelAdmin):
    pass

admin.site.register(School)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(Membership)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(Game)
admin.site.register(Forfeit)
