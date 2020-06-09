from django.db.models import (
    F, 
    ExpressionWrapper, 
    FloatField
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.
from .forms import (
    NewPurchaseForm,
    NewPurchaseDetailForm,
    PurchaseDetailInlineFormSet
)
from .models import (
    Supplier, 
    Purchase,
    Product
)

def get_all_suppliers(request):
    return render(request, 'suppliers/suppliers.html', {
        'suppliers': Supplier.objects.all()
    })

def get_purchases(request):
    return render(request, 'suppliers/purchases.html', {
        'purchases': Purchase.objects.all()
    })

def get_purchase_detail(request, pk):
    
    purchase = Purchase.objects.get(pk=pk)

    totals = Purchase.objects.get(pk=pk).products_purchased.all().annotate(
        total=ExpressionWrapper(
            F('cost') * F('quantity'), output_field=FloatField()
        )
    )
    total_purchased = 0
    for i in totals:
        total_purchased += i.total

    return render(request, 'suppliers/purchase-detail.html', {
        'products_purchased': totals,
        'total_purchased': total_purchased
    })

def new_purchase(request):

    if request.method == 'POST':
        form = NewPurchaseForm(request.POST)
        
        if form.is_valid():
            purchase = form.save(commit=False)
            formset = PurchaseDetailInlineFormSet(request.POST, instance=purchase)

            if formset.is_valid():
                purchase.save()
                new_purchases = formset.save(commit=False)
                for new_purchase in new_purchases:
                    # increase the product stock
                    Product.objects.filter(id=new_purchase.product.id).update(stock=F('stock') + new_purchase.quantity)
                    new_purchase.save()

                return HttpResponseRedirect(reverse('suppliers:purchases'))

    return render(request, 'suppliers/purchase-add.html', {
        'form': NewPurchaseForm(),
        'formset': PurchaseDetailInlineFormSet()
    })

def delete_purchase(request, pk):
    purchase = Purchase.objects.get(pk=pk)

    if purchase is not None:
        purchase.delete()

        return HttpResponseRedirect(reverse('suppliers:purchases'))
    