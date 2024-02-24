from rest_framework import serializers

from cart.models import CartItem, Cart


class CartSerializer(serializers.ModelSerializer):
    subtotal_price = serializers.ReadOnlyField()
    total_count = serializers.ReadOnlyField()
    value_added_tax = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'subtotal_price', 'total_count', 'value_added_tax', 'total_price')


class CartItemSerializer(serializers.ModelSerializer):
    item_price = serializers.ReadOnlyField()
    order_price = serializers.ReadOnlyField()
    cart = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'item_price', 'order_price')

    def create(self, validated_data):
        product = validated_data.get('product')
        cart = validated_data.get('cart')

        instance, _ = self.Meta.model.objects.get_or_create(product=product, cart=cart, defaults={'quantity': 0})
        instance.quantity += validated_data.get('quantity')
        instance.save()

        return instance
