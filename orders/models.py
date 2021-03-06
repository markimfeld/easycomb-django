from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from clients.models import Customer
from inventory.models import Combo, Product

class Status(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Status"

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    paid_status = models.BooleanField(default=False)
    money_received = models.FloatField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    combos = models.ManyToManyField(Combo, through='OrderDetail')
    products = models.ManyToManyField(Product, through='OrderDetail')

    def __str__(self):
        return f'{self.id} - {self.customer.first_name}'


class OrderDetail(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, blank=True, null=True, related_name="get_orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='get_products')
    description = models.CharField(max_length=100, blank=True)
    price_combo = models.FloatField(default=0)
    price_product = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=1)  


    def __str__(self):
        msg = ''
        if self.combo is None:
            msg = f'Order: {self.order.id} - {self.product.name} - {self.price_product} - {self.quantity}'
        elif self.product is None:
            msg = f'Order: {self.order.id} - {self.combo.name} - {self.price_combo} - {self.quantity}'
        return msg


class Income(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='incomes')
    date = models.DateField()
    amount = models.FloatField(default=0)

    def __str__(self):
        return f'{self.amount}'
