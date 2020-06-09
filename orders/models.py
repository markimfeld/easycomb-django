from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from clients.models import Customer
from inventory.models import Combo, Product


class Order(models.Model):
    
    class Status(models.TextChoices):
        PREPARE = 'P', _('Preparar')
        ALREADY = 'A', _('Listo')
        DELIVERED = 'D', _('Entregado')

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PREPARE,
    )
    
    date = models.DateField(auto_now_add=True)
    paid_status = models.BooleanField(default=False)
    money_received = models.FloatField(default=0)
    total = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    combos = models.ManyToManyField(Combo, through='OrderDetail')
    products = models.ManyToManyField(Product, through='OrderDetail')


class OrderDetail(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)    