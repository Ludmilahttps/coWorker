from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Type(models.Model):
    name = models.CharField(max_length=100)

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.type_id:  # Verifica se o campo `type` não foi definido
            self.type_id = 1  # Define o valor padrão como 1
        super(Users, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)