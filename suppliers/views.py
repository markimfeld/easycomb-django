from django.contrib.auth.decorators import login_required
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
    PurchaseDetailInlineFormSet,
    NewSupplierForm
)
from .models import (
    Supplier, 
    Purchase,
    Product
)

@login_required
def get_all_suppliers(request):
    return render(request, 'suppliers/suppliers.html', {
        'suppliers': Supplier.objects.all()
    })

@login_required
def add_new_supplier(request):

    if request.method == 'POST':
        form = NewSupplierForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('suppliers:suppliers'))

    return render(request, 'suppliers/supplier-add.html', {
        'form': NewSupplierForm()
    })

@login_required
def delete_supplier(request, pk):
    supplier = Supplier.objects.get(pk=pk)

    if supplier is not None:
        supplier.delete()

        return HttpResponseRedirect(reverse('suppliers:suppliers'))

@login_required
def edit_supplier(request, pk):
    supplier = Supplier.objects.get(pk=pk)

    if request.method == 'POST':
        
        form = NewSupplierForm(request.POST, instance=supplier)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('suppliers:suppliers'))

    return render(request, 'suppliers/supplier-edit.html', {
        'supplier': supplier,
        'form': NewSupplierForm(instance=supplier)
    })

@login_required
def get_purchases(request):
    return render(request, 'suppliers/purchases.html', {
        'purchases': Purchase.objects.all()
    })

@login_required
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

@login_required
def add_new_purchase(request):

    if request.method == 'POST':
        form = NewPurchaseForm(request.POST)
        
        print(form.is_valid())

        if form.is_valid():
            purchase = form.save()
            formset = PurchaseDetailInlineFormSet(request.POST, instance=purchase)
            if formset.is_valid():
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

@login_required
def delete_purchase(request, pk):
    purchase = Purchase.objects.get(pk=pk)

    if purchase is not None:
        purchase.delete()

        return HttpResponseRedirect(reverse('suppliers:purchases'))
    
