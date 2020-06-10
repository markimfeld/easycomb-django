from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField
)
from django.shortcuts import render

# Create your views here.
from .models import Order


def get_all_orders(request):
    return render(request, 'orders/orders.html', {
        'orders': Order.objects.filter(status='P').all()
    })

def get_order_details(request, pk):
    
    order = Order.objects.get(pk=pk)

    # get order's details and calculate subtotals
    order_details = order.get_combos.all().annotate(
        subtotal = ExpressionWrapper(
            F('price_unit') * F('quantity'), output_field=FloatField()
        )
    )

    total_items = 0
    for order_detail in order.get_combos.all():
        total_items += order_detail.quantity
    
    total = 0
    for order_detail in order_details:
        total += order_detail.subtotal


    return render(request, 'orders/order-details.html', {
        'total': total,
        'total_items': total_items,
        'order': order,
        'order_details': order_details
    })