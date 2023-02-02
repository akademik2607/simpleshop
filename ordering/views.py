from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from cart.workers import get_cart
from ordering.models import Order
from ordering.serializers import OrderSerializer
from ordering.workers import save_order_cart


class OrderView(CreateAPIView):
    models = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        cart = get_cart(request.session)
        if cart is None or cart['total_sum'] == '0':
            return Response({'error': 'your cart is  empty'})
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(request.session, serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, session, serializer):
        order = serializer.save()
        save_order_cart(session, order)
