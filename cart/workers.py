import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder

from cart.models import Product, ProductKit


def create_cart(session):
    session['cart'] = {'products': {}, 'total_sum': 0}
    return session['cart']


def get_cart(session):
    cart = session.get('cart', None)
    if cart:
        total_sum = 0
        for title, prod in cart['products'].items():
            if isinstance(prod, str):
                cart['products'][title] = json.loads(prod)
            else:
                cart['products'][title] = prod
            total_sum += Decimal(cart['products'][title]['sum'])
        cart['total_sum'] = str(total_sum)
        return cart
    else:
        return create_cart(session)


def add_product(title: str, count: int):
    if count == 0:
        return None
    product = Product.objects.get(title=title)
    product_kits = ProductKit.objects.filter(product=product).order_by('-product_count')
    temp_count = count
    product_info = {
        'packagings': {},
        'sum': 0,
        'unit': product.unit.title
    }
    for kit in product_kits:
        kit_count = kit.product_count
        if temp_count >= kit_count:
            cur_count = temp_count // kit.product_count
            kit_sum = kit.price * cur_count
            product_info['packagings'][kit.packaging.title] = {
                'article': kit.article,
                'price': kit.price,
                'count': cur_count,
                'sum': kit_sum}
            product_info['sum'] += kit_sum
            temp_count %= kit_count
    return product_info


def add_to_cart_product(session, product: dict, title: str):
    cart = get_cart(session)
    if not cart:
        cart = create_cart(session)
    cart['products'][title] = json.dumps(product, cls=DjangoJSONEncoder)
    session['cart'] = cart


def remove_product(session, title):
    cart = get_cart(session)
    if cart is None:
        cart = create_cart(session)
    if title in cart['products'].keys():
        del cart['products'][title]
    session['cart'] = cart
    return cart


def clear_cart(session):
    create_cart(session)
    return session['cart']
