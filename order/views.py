from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.none()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, user=self.request.user, is_ordered=False)
        serializer.save(user=self.request.user, cart=cart, order_id=get_random_string(10), subtotal=cart.subtotal_price,
                        tax_amount=cart.value_added_tax)

    def perform_update(self, serializer):
        old_order = self.get_object()
        if old_order.is_paid:
            return old_order
        instance = serializer.save()
        if instance.is_paid:
            instance.status = 'finished'
            instance.save()

            cart = instance.cart
            for item in cart.items.all():
                item.order_price = item.product.price
                item.save()
            cart.is_ordered = True
            cart.save()

            self.request.session['cart_count'] = 0


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'order/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user, is_ordered=False)
        order, _ = Order.objects.update_or_create(cart=cart, user=request.user, is_paid=False,
                                                  defaults={'order_id': get_random_string(10),
                                                            'subtotal': cart.subtotal_price,
                                                            'tax_amount': cart.value_added_tax})

        context = {'order': order}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, user=request.user, pk=int(request.POST.get('id', 0)))
        bool_dict = {'true': True, 'false': False, 'True': True, 'False': False}
        is_paid = bool_dict.get(request.POST.get('is_paid', 'false'), False)

        if is_paid:
            order.is_paid = True
            order.status = 'finished'
            order.save()

            cart = order.cart
            for item in cart.items.all():
                item.order_price = item.product.price
                item.save()
            cart.is_ordered = True
            cart.save()

            request.session['cart_count'] = 0

        return HttpResponseRedirect(reverse_lazy('orders'))


class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
