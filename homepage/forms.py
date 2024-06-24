from django import forms
from .models import Trip, Workspace

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['user', 'name', 'start_date', 'end_date', 'city', 'country', 'neighborhood']

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        # fields = ['name', 'description', 'country', 'state', 'city', 'neighborhood', 'street', 'number', 'complement', 'workingHours', 'category']

        fields = ['name', 'description', 'country', 'state', 'city', 'neighborhood', 'street', 'number', 'postalCode', 'complement', 'workingHours', 'category']
