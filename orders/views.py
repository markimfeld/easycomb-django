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
    OrderDetailInlineFormSet
)
from clients.models import Customer
from inventory.models import Product
from .models import Order



def get_all_orders(request):
    return render(request, 'orders/orders.html', {
        'orders': Order.objects.filter(status='P').all()
    })

def get_order_details(request, pk):
    
    order = Order.objects.get(pk=pk)
    incomes = order.incomes.all()

    # get order's details and calculate subtotals
    order_details = order.get_products.all().annotate(
        subtotal_combos = ExpressionWrapper(
            F('price_combo') * F('quantity'), output_field=FloatField()
        ),
        subtotal_products = ExpressionWrapper(
            F('price_product') * F('quantity'), output_field=FloatField()
        )
    )

    quantity_sum = order.get_products.all().aggregate(Sum('quantity'))

    total_combo = order_details.aggregate(Sum('subtotal_combos'))
    total_products = order_details.aggregate(Sum('subtotal_products'))

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
            new_order = form.save()
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

def delete_order(request, pk):
    order = Order.objects.get(pk=pk)

    if order is not None:
        order.delete()

        return HttpResponseRedirect(reverse('orders:orders'))