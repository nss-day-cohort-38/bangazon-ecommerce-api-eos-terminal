"""Product Types for Bangazon LLC"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Product Types

    Arguments:
        serializers
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'products')
        depth = 1


class ProductTypes(ViewSet):
    """Product Types for Bangazon LLC"""



    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized product type instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to Product Types resource

        Returns:
            Response -- JSON serialized list of Product Types
        """
        product_types = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            product_types, many=True, context={'request': request})
        return Response(serializer.data)