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
