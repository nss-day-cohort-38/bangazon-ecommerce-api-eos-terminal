from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from .customer import Customer
from .paymentType import PaymentType

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        ordering = (F('created_at').asc(nulls_last=True),)

    def __str__(self):
        return self.created_at


