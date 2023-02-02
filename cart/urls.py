from django.urls import path

from cart.views import ProductListView, CartView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('cart/', CartView.as_view()),
]
