from django.db import models

class Trip(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='trips/', blank=True, null=True)

    def __str__(self):
        return self.title
