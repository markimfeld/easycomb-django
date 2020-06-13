from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField,
    Sum
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.
from .models import Customer
from .forms import NewCustomerForm

def calculate_total_orders(orders):
    total = 0
    for order in orders:
        order_details = order.get_products.all().annotate(
            subtotal_combos = ExpressionWrapper(
                F('price_combo') * F('quantity'), output_field=FloatField()
            ),
            subtotal_products = ExpressionWrapper(
                F('price_product') * F('quantity'), output_field=FloatField()
            )
        )
        total += order_details.aggregate(Sum('subtotal_combos'))['subtotal_combos__sum']
        total += order_details.aggregate(Sum('subtotal_products'))['subtotal_products__sum']
    

    return total

def get_all_clients(request):
    return render(request, 'clients/customers.html', {
        'customers': Customer.objects.all()
    })

def get_customer_details(request, pk):
    customer = Customer.objects.get(pk=pk)

    total_to_paid = calculate_total_orders(customer.orders.filter(paid_status=False).all())
    print(total_to_paid)

    return render(request, 'clients/customer-details.html', {
        'customer': customer,
        'orders': customer.orders.all(),
        'total_to_paid': total_to_paid
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