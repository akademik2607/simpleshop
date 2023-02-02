from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Product
from cart.serializers import ProductSerializer, ProductAddSerializer
from cart.workers import add_product, add_to_cart_product, get_cart, clear_cart, remove_product


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(APIView):
    serializer_class = ProductAddSerializer

    def get(self, request, *args, **kwargs):
        cart = get_cart(request.session)
        return Response({'cart': cart})

    def post(self, request, *args, **kwargs):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            product = add_product(**serializer.data)
            title = serializer.data.get('title')
            if product:
                add_to_cart_product(request.session, product, title)
            else:
                remove_product(request.session, title)
            return Response({title: product})

        return Response({'errors': serializer.errors})

    def delete(self, request, *args, **kwargs):
        clear_cart(request.session)
        return Response(request.session)


