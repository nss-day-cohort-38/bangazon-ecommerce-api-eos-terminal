from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer
from django.contrib.auth.models import User

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'url', 'address', 'phone_number', 'user')
        depth = 1


class AccountView (ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order item
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(
                customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        """Handle GET requests to customers resource
        
        Returns:
            Response -- JSON serialized list of customers
        """

        customer = Customer.objects.get(user=request.auth.user)

        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual order item
        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        user.last_name = request.data["lastName"]
        user.save()
        customer.user = user
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone"]
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


