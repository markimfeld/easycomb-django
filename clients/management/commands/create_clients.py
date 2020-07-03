import random

from django.core.management.base import BaseCommand

from clients.models import Customer


class Command(BaseCommand):
    help = 'Creates clients for testing'

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
