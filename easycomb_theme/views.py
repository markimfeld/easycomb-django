from django.shortcuts import render

# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order

def index(request):

    return render(request, 'easycomb_theme/index.html', {
        'orders': Order.objects.all(),
        'quantity_orders': Order.objects.filter(status='P').all().count,
        'quantity_products': Product.objects.all().count,
        'quantity_combos': Combo.objects.all().count,
        'quantity_customers': Customer.objects.filter(status=True).all().count
    })