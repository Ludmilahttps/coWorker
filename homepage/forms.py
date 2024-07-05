from django import forms
from .models import Trip, Workspace

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['user', 'name', 'start_date', 'end_date', 'city', 'country', 'neighborhood']

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'description', 'workingHours', 'category', 'phone', 'website']
        exclude = ['owner', 'averageRating', 'country', 'state', 'city', 'neighborhood', 'street', 'number', 'postalCode', 'complement', 'latitude', 'longitude', 'email']