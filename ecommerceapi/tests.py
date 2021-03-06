import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ecommerceapi.models import *
from django.contrib.auth.models import User
from datetime import datetime
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
            product_type_id= self.productType.id
            )
        

    def test_post_OrderProduct(self):
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
        
    def test_delete_order_product(self):

        order_product = OrderProduct.objects.create(
            product_id = self.product.id,
            order_id = self.order.id)

        # delete and response
        response = self.client.delete((reverse('orderproduct-detail', kwargs={"pk": 1})), order_product, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # print("response data: ", response.data)

        # checking that the response is 204
        self.assertEqual(response.status_code, 204)
        
        # making sure the response is empty
        self.assertEqual(len(response.data), 0)
        
        # testing that the order object was deleted
        self.assertEqual(OrderProduct.objects.count(), 0) 


class TestAccountInfo(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test', last_name='user')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=self.user.id, address="123", phone_number="ring ring")
        
        

    def test_put_AccountInfo(self):
        new_customer_info = {
              "lastName": "userx",
              "address": "123 main street",
              "phone": "1234567890"
            }
        
        response = self.client.put(
            reverse('account-detail', kwargs={"pk":1}), new_customer_info, HTTP_AUTHORIZATION='Token ' + str(self.token), content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('account-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["last_name"], "userx")
        self.assertEqual(response.data["address"], "123 main street")
        self.assertEqual(response.data["phone_number"], "1234567890")
        

class TestProduct(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test', last_name='user')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=self.user.id)
        self.productType = ProductType.objects.create(name = "electronics")

    def test_post_Product(self):
        new_product = {
            "title": "Product Name",
            "customer": self.customer.id,
            "price": 100.00,
            "description": "I am a product",
            "quantity": 1,
            "location": "Nashville, TN",
            "image": "product.png",
            "product_type_id": self.productType.id,
            "created_at": datetime.now() 
            }
        
        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        
    def test_delete_Product(self):

        product = Product.objects.create(
            title = "Product Name",
            customer = self.customer,
            price = 100.00,
            description = "I am a product",
            quantity = 1,
            location = "Nashville, TN",
            image = "product.png",
            product_type_id = self.productType.id,
            created_at = datetime.now()   
        )

        # delete and response
        response = self.client.delete((reverse('product-detail', kwargs={"pk": 1})), product, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # print("response data: ", response.data)

        # checking that the response is 204
        self.assertEqual(response.status_code, 204)
        
        # making sure the response is empty
        self.assertEqual(len(response.data), 0)
        
        # testing that the order object was deleted
        self.assertEqual(Product.objects.count(), 0)


class TestRecommendedProduct(TestCase):
    def setUp(self):
        self.username1 = 'testuser'
        self.password1 = 'foobar'
        self.username2 = 'testuser2'
        self.password2 = 'foobar2'

        self.user1 = User.objects.create_user(username=self.username1, password=self.password1, first_name='test', last_name='user')
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2, first_name='test2', last_name='user2')
        self.token = Token.objects.create(user=self.user1)
        self.recommended_user = Customer.objects.create(user_id=self.user1.id)
        self.logged_in_user = Customer.objects.create(user_id=self.user2.id)
        self.productType = ProductType.objects.create(name = "electronics")
        self.product = Product.objects.create(customer_id = self.recommended_user.id,
            title = "Test Phone",
            price= 800.00,
            description= "Super cool new tech.",
            quantity= 20,
            location= "America",
            image= "death_ray.jpeg",
            product_type_id= self.productType.id
            )
        

    def test_post_RecommendedProduct(self):
        new_recommended_product = {
              "logged_in_user_id": self.logged_in_user.id,
              "product_id": self.product.id,
              "recommended_user_id": self.recommended_user.id
            }
        
        response = self.client.post(
            reverse('recommendedproduct-list'), new_recommended_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(RecommendedProduct.objects.count(), 1)

        