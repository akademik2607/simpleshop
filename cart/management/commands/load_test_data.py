from django.core.management.base import BaseCommand

from cart.models import Unit, Product, Packaging, ProductKit


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_units()
        self.create_products()
        self.create_packaging()
        self.create_product_kit()


    def create_units(self):
        Unit.objects.bulk_create([
            Unit(title='кг'),
            Unit(title='шт')
        ])

    def create_products(self):
        kg = Unit.objects.get(title='кг')
        ed = Unit.objects.get(title='шт')

        Product.objects.bulk_create([
            Product(title='яблоки', description='описание яблок', unit=kg),
            Product(title='груши', description='описание груш', unit=kg),
            Product(title='стулья', description='описание стульев', unit=ed),
        ])


    def create_packaging(self):
        Packaging.objects.bulk_create([
            Packaging(title='единица'),
            Packaging(title='короб'),
            Packaging(title='палет'),
        ])

    def create_product_kit(self):
        apple = Product.objects.get(title='яблоки')
        pear = Product.objects.get(title='груши')
        chair = Product.objects.get(title='стулья')

        unit = Packaging.objects.get(title='единица')
        box = Packaging.objects.get(title='короб')
        pallet = Packaging.objects.get(title='палет')

        ProductKit.objects.bulk_create([
            ProductKit(article='a1', product=apple, packaging=unit, product_count=1, price=10),
            ProductKit(article='a2', product=apple, packaging=box, product_count=10, price=90),
            ProductKit(article='a3', product=apple, packaging=pallet, product_count=50, price=430),
            ProductKit(article='p1', product=pear, packaging=unit, product_count=1, price=20),
            ProductKit(article='p2', product=pear, packaging=box, product_count=10, price=185),
            ProductKit(article='p3', product=pear, packaging=pallet, product_count=50, price=610),
            ProductKit(article='c1', product=chair, packaging=unit, product_count=1, price=100),
            ProductKit(article='c2', product=chair, packaging=box, product_count=3, price=270),
            ProductKit(article='c3', product=chair, packaging=pallet, product_count=10, price=900),
            ]
        )
