from django.db.models import Count, Sum, Value as V
from django.db.models.functions import Coalesce
from django.shortcuts import render


# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order, Status

def index(request):

    orders = Order.objects.all()

    # get total combos sales, only if had sales
    combos = Combo.objects.annotate(sales=(Coalesce(Sum('order__get_products__quantity'), V(0)))).filter(sales__gt=0).order_by('-sales')

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
