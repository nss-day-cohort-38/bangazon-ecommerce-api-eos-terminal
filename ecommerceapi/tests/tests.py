# Create your tests here.
import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ecommerceapi.models import *
from django.contrib.auth.models import User

# from .views import <Why don't we need to do this?>

class TestOrderProduct(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test', last_name='user')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=self.user.id)
        self.order = Order.objects.create(customer_id = self.customer.id)
        self.productType = ProductType.objects.create(name = "electronics")
        self.product = Product.objects.create(customer_id = self.customer.id,
            title = "Test Phone",
            price= 800.00,
            description= "Super cool new tech.",
            quantity= 20,
            location= "America",
            image= "death_ray.jpeg",
            product_type_id= self.productType.id)
        
        
    def Test_post_order(self):
       
        response = self.client.post(
            reverse('order-list'), new_order, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Order.objects.count(), 1)

        self.assertEqual(Order.objects.get().customer_id, 1)
        
    def Test_post_product(self):
        
        new_product = {
            "id": 1,
            "title": "Test Phone",
            "customer": self.customer.id,
            "price": 800.00,
            "description": "Super cool new tech.",
            "quanitity": 20,
            "location": "America",
            "image": "death_ray.jpeg",
            "product_type": "http://127.0.0.1:8000/producttypes/3"
        }
        
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().customer_id, 1)

    def Test_post_OrderProduct(self):
        new_order_product = {
              "product_id": self.product.id,
              "order_id": self.order.id
            }
        
        response = self.client.post(
            reverse('orderproduct-list'), new_order_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderProduct.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.get().order_id, 1)
        
    def Test_delete_order_product(self):

        order_product = OrderProduct.objects.create(
            product_id = self.product.id,
            order_id = self.order.id)

        # delete and response
        response = self.client.delete((reverse('orderproduct-detail', kwargs={"pk": 1})), order, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # print("response data: ", response.data)

        # checking that the response is 204
        self.assertEqual(response.status_code, 204)
        
        # making sure the response is empty
        self.assertEqual(len(response.data), 0)
        
        # testing that the order object was deleted
        self.assertEqual(Order.objects.count(), 0) 