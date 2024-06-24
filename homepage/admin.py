from django.contrib import admin
from .models import Trip

class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'start_date', 'end_date', 'country', 'neighborhood')
    search_fields = ('name',)

admin.site.register(Trip, TripAdmin)
