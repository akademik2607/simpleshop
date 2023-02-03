from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Product
from cart.serializers import ProductSerializer, ProductAddSerializer
from cart.workers import add_product, add_to_cart_product, get_cart, clear_cart, remove_product


class ProductListView(ListAPIView):
    """
    returns the product catalog
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartView(APIView):
    """
    shows or modifies the cart in the session

    methods: get, post, delete
    """
    serializer_class = ProductAddSerializer

    def get(self, request, *args, **kwargs):
        """
        shows the current bucket in the session

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        cart = get_cart(request.session)
        return Response({'cart': cart})

    def post(self, request, *args, **kwargs):
        """
        creates or modifies a product in the shopping cart
        post-data: {
            "title": string
            "count": int
        }
        if the count is 0, the product is removed from the cart

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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
        """
        clears the cart

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        clear_cart(request.session)
        return Response(request.session)


