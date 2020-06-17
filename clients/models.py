from django.db import models

# Create your models here.
from easycomb_theme.models import City, Address

class Customer(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    status = models.BooleanField(default=True)
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        blank=True,
        null=True
    )
    address = models.ForeignKey(
        Address, 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


    def __str__(self):
        return f'{self.first_name} {self.last_name}'