from django.db import transaction
from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField,
    Sum
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.
from .forms import (
    NewOrderForm,
    OrderDetailInlineFormSet,
    NewIncomeForm,
    ChangeStatusOrderForm,
)
from clients.models import Customer
from inventory.models import Product
from .models import Order, Status


def is_valid_query(params):
    return params is not None and params != ''
    
def calculate_subtotals(order):
    order_details = order.get_products.all().annotate(
        subtotal_combos = ExpressionWrapper(
            F('price_combo') * F('quantity'), output_field=FloatField()
        ),
        subtotal_products = ExpressionWrapper(
            F('price_product') * F('quantity'), output_field=FloatField()
        )
    )
    return order_details

def get_all_orders(request):
    
    customers = Customer.objects.filter(status=True).all()

    status = Status.objects.all()

    customer_id = request.GET.get('customer')

    status_id = request.GET.get('status')

    orders = Order.objects.all()

    if is_valid_query(customer_id) and int(customer_id) > 0:
        orders = orders.filter(customer=customers.get(pk=customer_id)).all()

    if is_valid_query(status_id) and int(status_id) > 0:
        orders = orders.filter(status=status.get(pk=status_id))

    return render(request, 'orders/orders.html', {
        'status_choices': status,
        'customers': customers,
        'orders': orders
    })

def register_order_paid(request, pk):
    order = Order.objects.get(pk=pk)

    order_details = calculate_subtotals(order)

    total_combo = order_details.aggregate(Sum('subtotal_combos'))['subtotal_combos__sum']
    total_products = order_details.aggregate(Sum('subtotal_products'))['subtotal_products__sum']
    incomes_sum = order.incomes.all().aggregate(Sum('amount'))['amount__sum']
    if order.incomes.all().aggregate(Sum('amount'))['amount__sum'] is None:
        incomes_sum = 0.0

    if request.method == 'POST':
        form = NewIncomeForm(request.POST)

        if form.is_valid():
            new_income = form.save(commit=False)
            if new_income.amount > 0 and ((new_income.amount + incomes_sum) <= total_combo or (new_income.amount + incomes_sum) <= total_products):
                new_income.order = order
                new_income.save()
                return HttpResponseRedirect(reverse('orders:order_details', args=(pk,)))
            else:
                if new_income.amount == 0:
                    print('El monto tiene que ser mayor que cero')
                else:
                    print('El monto ingresado es mayor al total!')

    return render(request, 'orders/order-register-paid.html', {
        'order': order,
        'form': NewIncomeForm()
    })

def get_order_details(request, pk):
    
    order = Order.objects.get(pk=pk)
    incomes = order.incomes.all()

    # get order's details and calculate subtotals
    order_details = calculate_subtotals(order)

    quantity_sum = order.get_products.all().aggregate(Sum('quantity'))

    total_combo = order_details.aggregate(Sum('subtotal_combos'))
    total_products = order_details.aggregate(Sum('subtotal_products'))

    incomes_sum = order.incomes.all().aggregate(Sum('amount'))


    if not order.paid_status:
        if total_combo['subtotal_combos__sum'] == incomes_sum['amount__sum'] or total_products['subtotal_products__sum'] == incomes_sum['amount__sum']:
            order.paid_status = True
            order.save()

    return render(request, 'orders/order-details.html', {
        'combos_total': total_combo['subtotal_combos__sum'],
        'products_total': total_products['subtotal_products__sum'],
        'quantity_total': quantity_sum['quantity__sum'],
        'order': order,
        'incomes': incomes,
        'order_details': order_details
    })

# open a transaction
@transaction.atomic
def add_new_order(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST)

        if form.is_valid():
            sid = transaction.savepoint()
            new_order = form.save(commit=False)
            new_order.status = Status.objects.first()
            new_order.save()
            # transaction now contains new_order.save()
            formset = OrderDetailInlineFormSet(request.POST, instance=new_order)
            
            if formset.is_valid():
                order_items = formset.save(commit=False)
                for order_item in order_items:
                    has_stock = True
                    if order_item.combo is not None:
                        order_item.price_combo = order_item.combo.price
                        for combo_item in order_item.combo.products.all():
                            # if the stock is more than or equal to the quantity that was requested so its okay
                            if combo_item.product.stock >= (order_item.quantity * combo_item.quantity):
                                # decrease the product stock
                                Product.objects.filter(id=combo_item.product.id).update(stock=F('stock') - (order_item.quantity * combo_item.quantity))
                            else:
                                has_stock = False
                    if order_item.product is not None:
                        order_item.price_product = order_item.product.retail_price
                        # if the stock is more than or equal the quantity that was requested so its okay
                        if order_item.product.stock >= order_item.quantity:
                            # decrease the product stock
                            Product.objects.filter(id=order_item.product.id).update(stock=F('stock') - order_item.quantity)
                    print(has_stock)
                    if has_stock:
                        order_item.save()
                        transaction.savepoint_commit(sid)
                        return HttpResponseRedirect(reverse('orders:orders'))
                    else:
                        transaction.savepoint_rollback(sid)

    return render(request, 'orders/order-add.html', {
        'form': NewOrderForm(),
        'formset': OrderDetailInlineFormSet()
    })

def change_status_order(request, pk):
    order = Order.objects.get(pk=pk)

    if request.method == 'POST':
        form = ChangeStatusOrderForm(request.POST)

        if form.is_valid():
            new_status = form.cleaned_data['status']
            order.status = new_status
            order.save()
            return HttpResponseRedirect(reverse('orders:orders'))

    return render(request, 'orders/order-edit-status.html', {
        'order': order,
        'form': ChangeStatusOrderForm(initial = {'status': order.status })
    })

def delete_order(request, pk):
    order = Order.objects.get(pk=pk)

    if order is not None:
        for order_item in order.get_products.all():
            if order_item.combo is not None:
                for combo_item in order_item.combo.products.all():
                    Product.objects.filter(id=combo_item.product.id).update(stock=F('stock') + (order_item.quantity * combo_item.quantity))
            else:
                Product.objects.filter(id=order_item.product.id).update(stock=F('stock') + order_item.quantity)
        
        order.delete()

        return HttpResponseRedirect(reverse('orders:orders'))