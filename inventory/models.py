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
