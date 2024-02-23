from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from store.models import Product
from .models import Cart, CartItem


def get_user_cart(request):
    """Retrieves the shopping cart for the current user."""
    cart_id = None
    cart = None
    # If the user is logged in, then grab the user's cart info.
    if request.user.is_authenticated and not request.user.is_anonymous:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart()
            cart.save()
            request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.get(id=cart_id)
    return cart


def get_cart_count(request):
    cart = get_user_cart(request)
    total_count = 0
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        total_count += item.quantity
    return total_count


def update_cart_info(request):
    request.session['cart_count'] = get_cart_count(request)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/view_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_user_cart(self.request)
        cart_items = CartItem.objects.filter(cart=cart)
        order_total = Decimal(0.0)
        for item in cart_items:
            order_total += (item.product.price * item.quantity)
        context['cart_items'] = cart_items
        context['order_total'] = order_total
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        cart = get_user_cart(request)
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('qty', 1))

        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, defaults={'quantity': 0})
        cart_item.quantity += quantity
        cart_item.save()

        request.session['cart_count'] = request.session.get('cart_count', 0) + quantity
        update_cart_info(request)
        return HttpResponseRedirect(reverse_lazy('view-cart'))


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = cart_item.quantity
        cart_item.delete()

        request.session['cart_count'] = max(request.session.get('cart_count', 0) - quantity, 0)
        update_cart_info(request)
        return HttpResponseRedirect(reverse_lazy('view-cart'))
