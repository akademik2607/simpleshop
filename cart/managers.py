from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().select_related('unit')


class ProductKitManager(models.Manager):
    def get_queryset(self):
        return super(ProductKitManager, self).get_queryset().select_related('product', 'packaging')


class ProductCountInOrderManager(models.Manager):
    def get_queryset(self):
        return super(ProductCountInOrderManager, self).get_queryset().select_related('product_kit', 'order')

