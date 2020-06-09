from django.shortcuts import render

# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo


def index(request):

    return render(request, 'easycomb_theme/index.html', {
        'quantity_products': Product.objects.all().count,
        'quantity_combos': Combo.objects.all().count,
        'quantity_customers': Customer.objects.all().count
    })