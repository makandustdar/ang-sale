from django.contrib import admin
from .models import OrderItem, OrderItemDetail, Order, OrderConfirmationCode, Clue, FeatureValue


class OrderAdmin(admin.ModelAdmin):
    list_display = 'user', 'transId', 'id'
    list_filter = ['expert']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['productName', 'order', 'quantity', 'id']


class OrderItemDetailAdmin(admin.ModelAdmin):
    list_display = ['feature', 'orderitem', 'orderitem_id']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemDetail, OrderItemDetailAdmin)
admin.site.register(OrderConfirmationCode)
admin.site.register(Clue)
admin.site.register(FeatureValue)
