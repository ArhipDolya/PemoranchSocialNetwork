from django.contrib import admin

from .models import Pemoran, PemoranLike


class PemoranLikeAdmin(admin.TabularInline):
    model = PemoranLike


class PemoranAdmin(admin.ModelAdmin):
    inlines = [PemoranLikeAdmin]
    list_display = ('__str__', 'user')
    search_fields = ('content', 'user__username', 'user__email')

    class Meta:
        model = Pemoran


admin.site.register(Pemoran, PemoranAdmin)
