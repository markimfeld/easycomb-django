from django.contrib import admin

# Register your models here.
from .models import City, Address

admin.site.register(City)
admin.site.register(Address)