from django.contrib import admin

# Register your models here.
from .models import *

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseDetailInline,
    ]

admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail)
