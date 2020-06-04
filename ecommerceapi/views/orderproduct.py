from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Customer, Order, OrderProduct, PaymentType, Product

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order_id', 'product_id', 'product')
        depth = 1
        
class OrderProducts(ViewSet):
    
    def create(self, request):
        customer = Customer.objects.get(user_id=request.auth.user.id)
        
        try:
            order = Order.objects.get(customer_id=customer.id, payment_type=None)
            
            new_order_product = OrderProduct()
            new_order_product.product_id = request.data['product_id']
            new_order_product.order_id = order.id
            
            new_order_product.save()

            serialize = OrderProductSerializer(new_order_product, context={'request': request}) 
        except:
            new_order = Order()
            new_order.customer_id = customer.id
            new_order.save()

            new_order_product = OrderProduct()
            new_order_product.product_id = request.data['product_id']
            new_order_product.order_id = new_order.id

            new_order_product.save()

            serialize = OrderProductSerializer(new_order_product, context={'request': request}) 

        return Response(serialize.data) 
    
    def list(self, request):
        #  def get_queryset(self):
        # queryset = Purchase.objects.all()
        # username = self.request.query_params.get('username', None)
        # if username is not None:
        #     queryset = queryset.filter(purchaser__username=username)
        # return queryset
        customer = Customer.objects.get(user=request.auth.user)
        order = Order.objects.get(customer_id=customer.id)
        order_products = OrderProduct.objects.filter(order_id=order.id)
        # user = self.request.query_params.get('user', None)
        # if user is not None:
            
        serializer = OrderProductSerializer(
            order_products, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
            
    
    def destroy(self, request, pk=None):

        try:
            orderproduct = OrderProduct.objects.get(pk=pk)
            orderproduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)