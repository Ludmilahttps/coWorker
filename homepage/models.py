from django.db import models
from django.utils import timezone

class Type(models.Model):
    name = models.CharField(max_length=100)

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    neighborhood = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    complement = models.CharField(max_length=100, blank=True, null=True)
    postalCode = models.CharField(max_length=20, blank=True, null=True)  # Ajuste o nome da coluna
    workingHours = models.CharField(max_length=100, blank=True, null=True)  # Ajuste o nome da coluna
    averageRating = models.FloatField(blank=True, null=True)  # Ajuste o nome da coluna
    owner = models.ForeignKey('Users', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

class WorkspacePhoto(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    file = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

class Notes(models.Model):
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

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slots = models.IntegerField()
    status = models.CharField(max_length=20)

class Subscription(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

class Report(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=50)
    reason = models.TextField()
    date = models.DateTimeField(default=timezone.now)

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
