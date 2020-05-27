from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType, Customer
from datetime import datetime

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for payment types
    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name', 'account_number', 'expiration_date', 'customer_id', 'created_at')
        # depth = 1

class PaymentTypes(ViewSet):
    
    def list(self, request):
        """Handle GET requests to payment types resource
        
        Returns:
            Response -- JSON serialized list of payment types
        """

        customer = Customer.objects.get(user=request.auth.user)

        payment_types = PaymentType.objects.filter(customer=customer)

        serializer = PaymentTypeSerializer(payment_types, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single payment type
        
        Returns:
            Response -- JSON serialized payment type instance
        """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized PaymentType instance
        """
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.account_number = request.data["account_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]

        customer = Customer.objects.get(pk=request.data['customer_id'])
        new_payment_type.customer = customer

        new_payment_type.created_at = datetime.now()

        new_payment_type.save()

        serializer = PaymentTypeSerializer(new_payment_type, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code 
        """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)