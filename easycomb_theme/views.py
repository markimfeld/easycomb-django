from django.db.models import Count
from django.shortcuts import render


# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order, Status

def index(request):

    orders = Order.objects.all()
    combos = Combo.objects.annotate(Count('order'))
    print(combos.values_list('name', 'order__count'))
    
    status = Status.objects.first()

    return render(request, 'easycomb_theme/index.html', {
        'combos': combos,
        'products': Product.objects.all(),
        'orders': Order.objects.all(),
        'quantity_orders': Order.objects.filter(status=status).all().count,
        'quantity_products': Product.objects.all().count,
        'quantity_combos': Combo.objects.all().count,
        'quantity_customers': Customer.objects.filter(status=True).all().count
    })