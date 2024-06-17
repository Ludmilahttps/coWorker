from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'start_date', 'end_date', 'image']
