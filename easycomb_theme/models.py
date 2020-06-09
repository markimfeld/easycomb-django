from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Address(models.Model):
    street_name = models.CharField(max_length=64)
    street_number = models.IntegerField()
    neighborhood = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f'{self.street_number} {self.street_name}, {self.neighborhood}'