"""View module for handling requests about orders"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order, Customer, PaymentType


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id','url', 'payment_type', 'created_at',)
        depth = 2

class OrderItems(ViewSet):

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single order item
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order_item = Order.objects.get(pk=pk)
            serializer = OrderItemSerializer(
                order_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to order resource
        Returns:
            Response -- JSON serialized list of customer orders
        """
        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(customer=customer)
        serializer = OrderItemSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)


    def create(self, request):

        payment_type = PaymentType.objects.get(pk=request.data["payment_type_id"])
        customer = Customer.objects.get(user=request.auth.user)


        new_order_item = Order()
        new_order_item.starttime = request.data["starttime"]
        new_order_item.payment_type = payment_type
        new_order_item.customer = customer

        new_order_item.save()

        serializer = OrderItemSerializer(
            new_order_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual order item
        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.starttime = request.data["starttime"]
        payment_type = PaymentType.objects.get(pk=request.data["payment_type_id"])
        order.payment_type = payment_type
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order item
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)