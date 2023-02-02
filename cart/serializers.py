from rest_framework import serializers

from cart.models import Product, ProductKit
from cart.validators import HasPosition


class ProductKitSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    packaging = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )
    count_in_package = serializers.SerializerMethodField()

    class Meta:
        model = ProductKit
        fields = ('article', 'product', 'count_in_package', 'packaging', 'price')

    def get_count_in_package(self, obj):
        return obj.product_count


class ProductSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('title', 'description', 'unit', 'sets')

    def get_sets(self, obj):
        products = ProductKitSerializer(obj.productkit_set.all(), many=True)
        return products.data


class ProductAddSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=200,
        required=True,
        validators=[HasPosition(Product.objects.all(), 'title')])
    count = serializers.IntegerField(min_value=0)


class DeleteProductInCartSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=200,
        required=True,
        validators=[HasPosition(Product.objects.all(), 'title')])
    count = serializers.IntegerField(allow_null=True)
