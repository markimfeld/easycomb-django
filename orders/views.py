from django.shortcuts import render

# Create your views here.
from .models import Order


def get_all_orders(request):
    return render(request, 'orders/orders.html', {
        'orders': Order.objects.filter(status='P').all()
    })