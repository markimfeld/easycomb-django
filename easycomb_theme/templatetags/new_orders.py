from django import template


register = template.Library()

from orders.models import Order, Status

@register.simple_tag
def new_orders():
    status = Status.objects.first()
    return Order.objects.filter(status=status).count()
