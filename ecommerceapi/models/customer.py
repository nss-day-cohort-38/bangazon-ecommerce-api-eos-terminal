from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=55)

    class Meta:
        ordering = (F('user.last_login').asc(nulls_last=True),)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


