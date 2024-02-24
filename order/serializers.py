from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.ReadOnlyField()
    order_id = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()
    cart = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_id', 'cart', 'status', 'subtotal', 'tax_amount', 'total', 'is_paid')

    def create(self, validated_data):
        cart = validated_data.get('cart')
        user = validated_data.get('user')
        order_id = validated_data.get('order_id')
        subtotal = validated_data.get('subtotal')
        tax = validated_data.get('tax_amount')
        instance, _ = Order.objects.update_or_create(cart=cart, user=user, is_paid=False,
                                                     defaults={'order_id': order_id,
                                                               'subtotal': subtotal,
                                                               'tax_amount': tax})

        return instance
