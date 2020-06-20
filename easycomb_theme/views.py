from django.db.models import Count, Sum
from django.shortcuts import render


# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order, Status

def index(request):

    orders = Order.objects.all()
    # combos = Combo.objects.annotate(Count('order'))
    combos_sales = [(combo, combo.get_orders.all().aggregate(total=Sum('quantity'))) for combo in Combo.objects.all()]
    # combos = [(combo_sale[0], combo_sale[1]['total']) for combo_sale in combos_sales]
    combos = []
    for combo_sale in combos_sales:
        if combo_sale[1]['total'] is not None:
            combos.append({'combo': combo_sale[0], 'sales': combo_sale[1]['total']})


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