from django.shortcuts import render

# Create your views here.
from .models import Customer

def get_all_clients(request):
    return render(request, 'clients/customers.html', {
        'customers': Customer.objects.all()
    })

def edit_customer(request, pk):
    pass

def delete_customer(request, pk):
    pass