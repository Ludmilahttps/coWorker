from django.db import models
from django.utils import timezone
from accounts.models import Users, Type
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Workspace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    complement = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    workingHours = models.CharField(max_length=100, blank=True, null=True)
    averageRating = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    note_sockets = models.IntegerField()
    note_internet = models.IntegerField()
    note_silence = models.IntegerField()
    note_menu_price = models.IntegerField()
    note_daily_price = models.IntegerField()
    note_general = models.IntegerField()

class Rating(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    useful_count = models.IntegerField(default=0)

class ReviewVote(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    review = models.ForeignKey(Rating, related_name='votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=[('upvote', 'Upvote'), ('downvote', 'Downvote')])
    date = models.DateTimeField(default=timezone.now)
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slots = models.IntegerField()
    status = models.CharField(max_length=20)

class WorkspacePhoto(models.Model):
    workspace = models.ForeignKey(Workspace, related_name='photos', on_delete=models.CASCADE)
    review = models.ForeignKey('Rating', related_name='photos', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.FileField(upload_to='workspace_photos/')
    date_added = models.DateTimeField(auto_now_add=True)

# class Subscription(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20)

# class Report(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     content_type = models.CharField(max_length=50)
#     reason = models.TextField()
#     date = models.DateTimeField(default=timezone.now)

class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class LikedWorkspaces(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    like_date = models.DateTimeField(default=timezone.now)

class Trip(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    country = models.CharField(max_length=100, default='Unknown')
    neighborhood = models.CharField(max_length=100, default='Unknown')
    city = models.CharField(max_length=100, default='Unknown')
    name = models.CharField(max_length=100, default='Unknown')
