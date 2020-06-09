from django.shortcuts import render

# Create your views here.
from .models import Customer
from .forms import NewCustomerForm

def get_all_clients(request):
    return render(request, 'clients/customers.html', {
        'customers': Customer.objects.all()
    })

def add_new_customer(request):
    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

    return render(request, 'clients/customer-add.html', {
        'form': NewCustomerForm()
    })

def edit_customer(request, pk):
    pass

def delete_customer(request, pk):
    pass