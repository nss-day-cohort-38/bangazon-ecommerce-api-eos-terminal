"""Product for Bangazon LLC"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product as ProductModel


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
        fields = ('id', 'title', 'customer', 'price', 'description', 'quantity', 'location', 'image', 'created_at', 'product_type')


class Product(ViewSet):
    """Product for Bangazon LLC"""



    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized product type instance
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