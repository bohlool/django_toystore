from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]