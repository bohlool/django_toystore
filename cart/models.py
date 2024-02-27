from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product, TimeStampedModel

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return 'Cart #' + str(self.id)

    @property
    def subtotal_price(self):
        return sum(item.item_price for item in self.items.all())

    @property
    def total_count(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def value_added_tax(self):
        return round(self.subtotal_price * Decimal(0.09), 2)

    @property
    def total_price(self):
        return self.subtotal_price + self.value_added_tax


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_items')
    quantity = models.IntegerField(default=0)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return 'Item #' + str(self.id) + ': ' + self.product.title

    @property
    def item_price(self):
        return self.quantity * (self.product.price if not self.cart.is_ordered else self.order_price)
