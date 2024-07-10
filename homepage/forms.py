from django import forms
from .models import Trip, Workspace, Rating, Notes, WorkspacePhoto
from django.forms.models import inlineformset_factory

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['user', 'name', 'start_date', 'end_date', 'city', 'country', 'neighborhood']

class WorkspaceForm(forms.ModelForm):
    class Meta:
        model = Workspace
        fields = ['name', 'description', 'workingHours', 'category', 'phone', 'website']
        exclude = ['owner', 'averageRating', 'country', 'state', 'city', 'neighborhood', 'street', 'number', 'postalCode', 'complement', 'latitude', 'longitude', 'email']

class ReviewForm(forms.ModelForm):
    note_general = forms.IntegerField(min_value=0, max_value=5, label="General Rating")
    note_sockets = forms.IntegerField(min_value=0, max_value=5, label="Sockets Rating")
    note_internet = forms.IntegerField(min_value=0, max_value=5, label="Internet Rating")
    note_silence = forms.IntegerField(min_value=0, max_value=5, label="Silence Rating")
    note_menu_price = forms.IntegerField(min_value=0, max_value=5, label="Menu Price Rating")
    note_daily_price = forms.IntegerField(min_value=0, max_value=5, label="Daily Price Rating")

    class Meta:
        model = Rating
        fields = ['comment']
        labels = {
            'comment': 'Comment',
        }

class ReviewPhotoForm(forms.ModelForm):
    class Meta:
        model = WorkspacePhoto
        fields = ['file']

ReviewPhotoFormSet = forms.inlineformset_factory(Rating, WorkspacePhoto, form=ReviewPhotoForm, extra=5, max_num=5, can_delete=True)