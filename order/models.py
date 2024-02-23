from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Cart
from store.models import TimeStampedModel

User = get_user_model()

ORDER_STATUS = (
    ('started', 'Started'),
    ('abandoned', 'Abandoned'),
    ('finished', 'Finished'),
)


class Order(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')

    order_id = models.CharField(unique=True, max_length=120, default='abc')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default='started')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-pk',)

    @property
    def total(self):
        return self.subtotal + self.tax_amount

    def __str__(self):
        return '<Order:' + self.order_id + '> ' + self.status + ' | ' + str(self.created)
