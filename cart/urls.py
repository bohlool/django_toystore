from django.urls import path

from . import views

urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', views.CartView.as_view(), name='view-cart'),
]
