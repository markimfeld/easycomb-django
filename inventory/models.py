from django.db import models

# Create your models here.
from easycomb_theme.models import Address, City


default_product_image = 'uploads/default-product.jpg'


class Supplier(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.first_name


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    stock = models.IntegerField()
    wholesale_price = models.FloatField()
    retail_price = models.FloatField()
    image = models.ImageField(upload_to='uploads/', default=default_product_image)

    def __str__(self):
        return f'{self.name}'

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    products = models.ManyToManyField(Product, through='PurchaseDetail')

    def __str__(self):
        return f'{self.supplier} - {self.date}'


class PurchaseDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cost = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.purchase.supplier} {self.product.name} - {self.quantity} - ${self.cost}'

