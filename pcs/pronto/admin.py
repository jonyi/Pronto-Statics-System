from django.contrib import admin

from .models import Pronto


class ProntoAdmin(admin.ModelAdmin):
    list_display = ('title', 'reported_date', 'was_reported_recently')
    fieldsets = [
        ('Date information', {'fields': ['reported_date', 'pronto_id', 'release', 'feature', 'title',
                                         'build', 'severity', 'responsible_person',
                                         'status', 'transfer_from', 'transfer_to', 'rca_state',
                                         'rft_date', 'in_date', 'out_date', 'root_cause_found_date',
                                         'group_idx', 'is_top'], 'classes': ['collapse']}),
    ]

admin.site.register(Pronto, ProntoAdmin)
