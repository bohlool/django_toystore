from django.contrib.auth import get_user_model
from django.db import models

from store.models import Product, TimeStampedModel

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return 'Cart #' + str(self.id)


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_items')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return 'Item #' + str(self.id) + ': ' + self.product.name
