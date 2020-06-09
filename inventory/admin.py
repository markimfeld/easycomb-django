from django.contrib import admin

# Register your models here.
from .models import *

class ComboDetailInline(admin.TabularInline):
    model = ComboDetail

class ComboAdmin(admin.ModelAdmin):
    inlines = [
        ComboDetailInline,
    ]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Combo, ComboAdmin)
admin.site.register(ComboDetail)
