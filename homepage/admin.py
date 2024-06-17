from django.contrib import admin
from .models import Trip

class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    search_fields = ('title',)

admin.site.register(Trip, TripAdmin)
