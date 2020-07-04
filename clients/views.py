from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField,
    Sum,
    Value as V
)
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

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

        money_received = order.incomes.all().aggregate(total=Coalesce(Sum('amount'), V(0)))
        total -= money_received['total']

    return total

class CustomerListView(ListView):
    model = Customer
    template_name = 'clients/customers.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomerListView, self).dispatch(request, *args, **kwargs)


@login_required
def get_customer_details(request, pk):
    customer = Customer.objects.get(pk=pk)

    total_to_paid = calculate_total_orders(customer.orders.filter(paid_status=False).all())
    print(total_to_paid)

    return render(request, 'clients/customer-details.html', {
        'customer': customer,
        'orders': customer.orders.all(),
        'total_to_paid': total_to_paid
    })

@login_required
def add_new_customer(request):
    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            if not Customer.objects.filter(first_name__iexact=customer.first_name, last_name__iexact=customer.last_name).exists():
                customer.save()
                messages.success(request, 'Cliente Registrado!')
                return HttpResponseRedirect(reverse('clients:customers'))
            else:
                messages.error(request, 'Ya existe un cliente con ese nombre y apellido!')

    return render(request, 'clients/customer-add.html', {
        'form': NewCustomerForm()
    })

@login_required
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

@login_required
def activate_customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    if customer is not None:
        customer.status = True
        customer.save()
        return HttpResponseRedirect(reverse('clients:customers'))

@login_required
def deactivate_customer(request, pk):
    customer = Customer.objects.get(pk=pk)

    if customer is not None:
        customer.status = False
        customer.save()
        return HttpResponseRedirect(reverse('clients:customers'))

