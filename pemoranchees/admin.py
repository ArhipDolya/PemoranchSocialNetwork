from django.contrib import admin

from .models import Pemoran


class PemoranAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')
    search_fields = ('content', 'user__username', 'user__email')

    class Meta:
        model = Pemoran


admin.site.register(Pemoran, PemoranAdmin)
