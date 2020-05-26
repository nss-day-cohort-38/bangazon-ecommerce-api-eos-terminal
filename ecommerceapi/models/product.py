from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from .customer import Customer
from .productType import ProductType

class Product(models.Model):

    title = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    price = models.FloatField()
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    product_type = models.ForeignKey(ProductType, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = (F('created_at').asc(nulls_last=True),)


    def __str__(self):
        return self.title