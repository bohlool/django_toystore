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
    def total_price(self):
        return sum(item.item_price for item in self.items.all())

    @property
    def total_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_items')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return 'Item #' + str(self.id) + ': ' + self.product.name

    @property
    def item_price(self):
        return self.quantity * self.product.price
