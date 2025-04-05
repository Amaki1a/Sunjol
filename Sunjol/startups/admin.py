from django.contrib import admin
from .models import Startup

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'stage', 'founder', 'current_funding', 'funding_goal')
    list_filter = ('industry', 'stage')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'logo')
        }),
        ('Details', {
            'fields': ('industry', 'stage', 'founder')
        }),
        ('Funding', {
            'fields': ('current_funding', 'funding_goal')
        }),
    )
