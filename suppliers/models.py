from django.db import models

# Create your models here.
from easycomb_theme.models import Address, City
from inventory.models import Product



class Supplier(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=0)
    date = models.DateField()
    remarks = models.CharField(max_length=100, blank=True, null=True)
    products = models.ManyToManyField(Product, through='PurchaseDetail')

    def __str__(self):
        return f'{self.supplier} - {self.date}'


class PurchaseDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='products_purchased')
    description = models.CharField(max_length=100, blank=True, null=True)
    cost = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.purchase.supplier} {self.product.name} - {self.quantity} - ${self.cost}'
    