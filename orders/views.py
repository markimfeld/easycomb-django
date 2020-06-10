from django.db.models import (
    F,
    ExpressionWrapper,
    FloatField
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.
from .forms import (
    NewOrderForm,
    OrderDetailInlineFormSet
)
from .models import Order


def get_all_orders(request):
    return render(request, 'orders/orders.html', {
        'orders': Order.objects.filter(status='P').all()
    })

def get_order_details(request, pk):
    
    order = Order.objects.get(pk=pk)

    # get order's details and calculate subtotals
    order_details = order.get_combos.all().annotate(
        subtotal = ExpressionWrapper(
            F('price_unit') * F('quantity'), output_field=FloatField()
        )
    )

    total_items = 0
    for order_detail in order.get_combos.all():
        total_items += order_detail.quantity
    
    total = 0
    for order_detail in order_details:
        total += order_detail.subtotal


    return render(request, 'orders/order-details.html', {
        'total': total,
        'total_items': total_items,
        'order': order,
        'order_details': order_details
    })

def add_new_order(request):

    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            formset = OrderDetailInlineFormSet(request.POST, instance=new_order)
            
            if formset.is_valid():
                order_items = formset.save(commit=False)
                for order_item in order_items:
                    order_item.price_unit = 180
                    order_item.save()
                
                return HttpResponseRedirect(reverse('orders:orders'))
    
    return render(request, 'orders/order-add.html', {
        'form': NewOrderForm(),
        'formset': OrderDetailInlineFormSet()
    })