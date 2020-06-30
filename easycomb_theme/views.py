from django.db.models import Count, Sum, Value as V
from django.db.models.functions import Coalesce
from django.shortcuts import render

# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order, Status, OrderDetail

def index(request):

    orders = Order.objects.all()
    order_details = OrderDetail.objects.all().select_related('combo', 'order')
    # get total combos sales, only if had sales
    most_selled_combos = order_details.exclude(combo=None).values('combo__name', 'combo__price').annotate(total_sales=Coalesce(Sum('quantity'), V(0))).order_by('-total_sales')

    status = Status.objects.first()

    return render(request, 'easycomb_theme/index.html', {
        'most_selled_combos': most_selled_combos,
        'products': Product.objects.all(),
        'orders': Order.objects.all(),
        'quantity_orders': Order.objects.filter(status=status).all().count,
        'quantity_products': Product.objects.all().count,
        'quantity_combos': Combo.objects.all().count,
        'quantity_customers': Customer.objects.filter(status=True).all().count
    })


