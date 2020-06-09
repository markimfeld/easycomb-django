from django.db import models

# Create your models here.
from easycomb_theme.models import Address, City

default_product_image = 'uploads/default-product.jpg'

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
    stock = models.IntegerField(default=0)
    wholesale_price = models.FloatField()
    retail_price = models.FloatField()
    image = models.ImageField(upload_to='uploads/', default=default_product_image)

    def __str__(self):
        return f'{self.name}'


class Combo(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()
    product_list = models.ManyToManyField(Product, through='ComboDetail')

    def __str__(self):
        return self.name


class ComboDetail(models.Model):
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.combo.name} - {self.product.name} - {self.quantity}'