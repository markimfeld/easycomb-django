from django.test import TestCase

from easycomb_theme.models import Address, City
from suppliers.models import Supplier

class YourTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(street_name='San Martin', street_number=12, neighborhood='Centro')
        city = City.objects.create(name='Saenz Peña')
        Supplier.objects.create(first_name='Gustavo', last_name='Paszco', phone='3644878945', address=address, city=city)

    def test_first_name_label(self):
        """Check if first_name label is ok"""
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_first_name_max_length(self):
        """Check if first_name length is 50"""
        supplier = Supplier.objects.get(id=1)
        max_length = supplier._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 64)
    
    def test_last_name_label(self):
        supplier = Supplier.objects.get(id=1)
        field_label = supplier._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_last_name_max_length(self):
        supplier = Supplier.objects.get(id=1)
        max_length = supplier._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 64)