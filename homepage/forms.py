from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['user', 'name', 'start_date', 'end_date', 'city', 'country', 'neighborhood']
