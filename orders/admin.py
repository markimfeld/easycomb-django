from django.contrib import admin

# Register your models here.
from .models import (
    Order, 
    OrderDetail,
    Income,
    Status
)


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderDetailInline,
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)
admin.site.register(Income)
admin.site.register(Status)