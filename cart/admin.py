from django.contrib import admin

from cart.models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

    list_display = ('product', 'quantity', 'created', 'modified')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'created', 'modified')
