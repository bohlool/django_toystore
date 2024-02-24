from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.filter(is_ordered=False)
    serializer_class = CartSerializer

    @action(detail=True)
    def items(self, request, *args, **kwargs):
        cart = self.get_object()
        return Response(CartItemSerializer(cart.items.all(), many=True).data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.none()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = get_user_cart(self.request)
        return cart.items.all()

    def perform_create(self, serializer):
        instance = serializer.save(cart=get_user_cart(self.request))
        update_cart_info(self.request, instance.cart)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save(cart=get_user_cart(self.request))
        update_cart_info(self.request, instance.cart)
        return instance

    def perform_destroy(self, instance):
        cart = instance.cart
        super().perform_destroy(instance)
        update_cart_info(self.request, cart)


def get_user_cart(request):
    """Retrieves the shopping cart for the current user."""
    try:
        cart = Cart.objects.get(user=request.user, is_ordered=False)
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()
    return cart


def update_cart_info(request, cart):
    request.session['cart_count'] = cart.total_count


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/view_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = get_user_cart(self.request)
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        cart = get_user_cart(request)
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('qty', 1))

        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': 0})
        cart_item.quantity += quantity
        cart_item.save()

        update_cart_info(request, cart)
        return HttpResponseRedirect(reverse_lazy('view-cart'))


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart
        cart_item.delete()

        update_cart_info(request, cart)
        return HttpResponseRedirect(reverse_lazy('view-cart'))
