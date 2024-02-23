from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'modified', 'cart', 'status', 'subtotal', 'tax_amount', 'total')
    list_display_links = ('id', 'order_id')
    list_filter = ('status',)
    search_fields = ('order_id',)
    date_hierarchy = 'created'
