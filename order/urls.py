from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('api/order/', include(router.urls)),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
