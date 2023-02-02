from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class HasPosition:
    def __init__(self, queryset, field):
        self.queryset = queryset
        self.field = field

    def __call__(self, value):
        query_filter = {self.field: value}
        try:
            self.queryset.get(**query_filter)
        except ObjectDoesNotExist:
            message = 'There is no such this position'
            raise serializers.ValidationError(message)
