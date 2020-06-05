from django.db import models
from .customer import Customer
from .product import Product

class RecommendedProduct(models.Model):

    recommended_user = models.ForeignKey(Customer, related_name='recommneded_user', on_delete=models.CASCADE)
    logged_in_user = models.ForeignKey(Customer, related_name='logged_in_user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


