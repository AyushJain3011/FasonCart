from django.contrib import admin


from .models import ShippingAddress, Order, OrderItem

# Register your models here.

# @admin.register(ShippingAddress)
# class ShippingAddressAdmin(admin.ModelAdmin):

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

