from django.shortcuts import render

# Create your views here.
from inventory.models import Product

def index(request):

    return render(request, 'easycomb_theme/index.html', {
        'products': Product.objects.all()
    })