"""
url:
    '' - catalog
    'cart/' - viewing, creating, modifying, and deleting a cart
    'order/' - creating an order
"""

from django.contrib import admin
from django.urls import path, include

from ordering.views import OrderView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('order/', OrderView.as_view()),
]
