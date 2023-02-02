from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    AWAIT = 'aw'
    ACTIVE = 'act'
    COMPLETE = 'comp'

    STATUSES = (
        (AWAIT, 'ожидает'),
        (ACTIVE, 'активный'),
        (COMPLETE, 'завершён')
    )
    name = models.CharField(max_length=50, verbose_name='Имя')
    lastname = models.CharField(max_length=50, verbose_name='Фамилия')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    email = models.EmailField(verbose_name='Email')
    phone = PhoneNumberField(verbose_name='Телефон')
    status = models.CharField(choices=STATUSES, max_length=4, verbose_name='Статус', default=AWAIT)
