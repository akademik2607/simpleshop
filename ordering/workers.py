from django.db import transaction

from cart.models import ProductKit, Product, Packaging, ProductCountInOrder
from cart.workers import get_cart


@transaction.atomic
def save_order_cart(session, order):
    cart = get_cart(session)
    if cart is None:
        return False
    product_kits = []
    product_kits_counts = []
    for title, packagings in cart['products'].items():
        product = Product.objects.get(title=title)
        for kit_title, kit_val in packagings['packagings'].items():
            packaging = Packaging.objects.get(title=kit_title)
            product_kit = ProductKit.objects.filter(product=product, packaging=packaging)
            product_kits.append(product_kit)
            product_kits_counts.append(kit_val['count'])

    products_in_order = []
    for i, kit in enumerate(product_kits):
        products_in_order.append(ProductCountInOrder(order=order, product_kit=kit[0], count=product_kits_counts[i]))
    ProductCountInOrder.objects.bulk_create(products_in_order)

