from django.db import models

from cart.managers import ProductManager, ProductKitManager, ProductCountInOrderManager
from ordering.models import Order


NULLABLE = {'null': True, 'blank': True}


class Unit(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')
    unit = models.ForeignKey('unit', on_delete=models.CASCADE, verbose_name='Единица измерения')

    objects = ProductManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Packaging(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Упаковка'


class ProductKit(models.Model):
    article = models.CharField(max_length=150, unique=True)
    product = models.ForeignKey('product', on_delete=models.CASCADE, verbose_name='Товар')
    packaging = models.ForeignKey('packaging', on_delete=models.CASCADE, verbose_name='Упаковка')
    product_count = models.IntegerField(verbose_name='Количество товара', default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    objects = ProductKitManager()


class ProductCountInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_kit = models.ForeignKey(ProductKit, on_delete=models.CASCADE, **NULLABLE)
    count = models.IntegerField(verbose_name='Количество')

    objects = ProductCountInOrderManager()
