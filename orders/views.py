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
    
    
    # subtotals = Order.objects.get(pk=pk).get_combos.all().annotate(
    #     subtotal = ExpressionWrapper(
    #         F()
    #     )
    # )


    return render(request, 'orders/order-details.html', {
        'order': Order.objects.get(pk=pk)
    })