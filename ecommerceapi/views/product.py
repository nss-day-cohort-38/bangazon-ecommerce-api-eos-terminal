"""Product for Bangazon LLC"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product as ProductModel
from ecommerceapi.models import ProductType, Customer
from datetime import datetime

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Product 

    Arguments:
        serializers
    """
    class Meta:
        model = ProductModel
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer', 'price', 'description', 'quantity', 'location', 'image', 'created_at', 'product_type', 'product_type_id')


class Product(ViewSet):
    """Product for Bangazon LLC"""



    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = ProductModel.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to Product  resource

        Returns:
            Response -- JSON serialized list of Product 
        """
        product = ProductModel.objects.all()
        serializer = ProductSerializer(
            product, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        product_type = ProductType.objects.get(pk=request.data["product_type_id"])
        customer = Customer.objects.get(user=request.auth.user)

        new_product = ProductModel()
        new_product.customer = customer
        new_product.created_at = datetime.now()
        new_product.product_type = product_type
        new_product.title = request.data["title"]
        new_product.price = request.data["price"]
        new_product.description = request.data["description"] 
        new_product.quantity = request.data["quantity"]
        new_product.location = request.data["location"]
        new_product.image = request.data["image"]

        new_product.save()

        serializer = ProductSerializer(
            new_product, context={'request': request}
        )

        return Response(serializer.data)

