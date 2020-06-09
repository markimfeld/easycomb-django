from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

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
            form.save()
            return HttpResponseRedirect(reverse('clients:customers'))

    return render(request, 'clients/customer-add.html', {
        'form': NewCustomerForm()
    })

def edit_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('clients:customers'))


    return render(request, 'clients/customer-edit.html', {
        'customer': customer,
        'form': NewCustomerForm(instance=customer)
    }) 

def activate_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    if customer is not None:
        customer.status = True
        customer.save()
        return HttpResponseRedirect(reverse('clients:customers'))

def deactivate_customer(request, pk):
    customer = Customer.objects.get(pk=pk)

    if customer is not None:
        customer.status = False
        customer.save()
        return HttpResponseRedirect(reverse('clients:customers'))