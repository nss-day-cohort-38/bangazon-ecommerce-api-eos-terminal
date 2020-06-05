"""View module for handling requests about recommended_products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import RecommendedProduct, Customer, Product
from datetime import datetime
from django.contrib.auth.models import User



class RecommendedProductItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for recommended_products
    Arguments:
        serializers
    """

    class Meta:
        model = RecommendedProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='recommended_product',
            lookup_field='id'
        )
        fields = ('id','url', 'product', 'logged_in_user', 'recommended_user',)
        depth = 1

class RecommendedProductItems(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single recommended_product item
        Returns:
            Response -- JSON serialized recommended_product instance
        """
        try:
            recommended_product_item = RecommendedProduct.objects.get(pk=pk)
            serializer = RecommendedProductItemSerializer(
                recommended_product_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def list(self, request):
        """Handle GET requests to order resource
        Returns:
            Response -- JSON serialized list of customer recommended_product
        """
        recommended_user = Customer.objects.get(user=request.auth.user)
        recommended_products = RecommendedProduct.objects.filter(recommended_user=recommended_user)
        serializer = RecommendedProductItemSerializer(
            recommended_products, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):

        logged_in_user = Customer.objects.get(user=request.auth.user)
        product = Product.objects.get(pk=request.data["product_id"])
        recommended_user = Customer.objects.get(pk=request.data["recommended_user_id"])


        new_recommended_product_item = RecommendedProduct()
        new_recommended_product_item.product = product
        new_recommended_product_item.logged_in_user_id = logged_in_user.id
        new_recommended_product_item.recommended_user_id = recommended_user.id


        new_recommended_product_item.save()

        serializer = RecommendedProductItemSerializer(
            new_recommended_product_item, context={'request': request})

        return Response(serializer.data)
