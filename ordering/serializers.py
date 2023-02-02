from rest_framework import serializers

from ordering.models import Order


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=9, read_only=True)
    product_set = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('name', 'lastname', 'address', 'email', 'phone', 'status', 'product_set')

    def get_product_set(self, obj):
        products_count_in_order = obj.productcountinorder_set.all()
        order = {}
        order['products'] = []
        total_sum = 0
        for prod_in_order in products_count_in_order:
            title = prod_in_order.product_kit.product.title
            packaging = prod_in_order.product_kit.packaging.title
            price = prod_in_order.product_kit.price
            count = prod_in_order.count
            total_sum += price * count
            product = {
                'product': title,
                'packaging': packaging,
                'price': price,
                'count': count,
            }
            order['products'].append(product)
        order['total_sum'] = total_sum
        return order

