from django.db import models

class Trip(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='trips/', blank=True, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/')
    
    def __str__(self):
        return self.name

class Workspace(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='workspace_images/')
    category = models.ForeignKey(Category, related_name='workspaces', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
# Discover screen
class UserType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'category'
    def __str__(self):
        return self.name

class Photo(models.Model):
    file = models.ImageField(upload_to='photos/')

    def __str__(self):
        return str(self.file)

class Workspace(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    complement = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
