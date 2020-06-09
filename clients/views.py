from django.shortcuts import render

# Create your views here.
from .models import Customer

def get_all_clients(request):
    return render(request, 'clients/clients.html', {
        'customers': Customer.objects.all()
    })