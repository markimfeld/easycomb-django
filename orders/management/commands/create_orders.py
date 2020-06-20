import random

from django.core.management.base import BaseCommand

from clients.models import Customer
from inventory.models import Combo
from orders.models import Order, OrderDetail, Status

status = Status.objects.all()
customers = Customer.objects.all()
combos = Combo.objects.all()

def get_random_combo():
    index = random.randint(0, len(combos) - 1)
    return combos[index]

def get_random_quantity():
    return random.randint(1, 10)

def get_random_status():
    index = random.randint(0, len(status) - 1)
    return status[index]

class Command(BaseCommand):
    help = 'Creates orders for testing'

    def handle(self, *args, **kwargs):
        for customer in customers:
            order = Order(
                status = get_random_status(),
                paid_status = False,
                customer = customer
            )
            order.save()
            
            combo = get_random_combo()
            order_detail = OrderDetail(
                order = order,
                combo = combo, 
                price_combo = combo.price,
                quantity = get_random_quantity()
            )

            order_detail.save()

            self.stdout.write(self.style.SUCCESS('Successfully created order "%s" ' % order.id))
        self.stdout.write(self.style.SUCCESS('------------------------------------'))
        self.stdout.write(self.style.SUCCESS('Creation completed successfully!'))