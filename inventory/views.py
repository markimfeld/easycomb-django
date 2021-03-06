from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import ( 
    NewProductForm,
    NewCategoryForm,
    NewComboForm,
    ComboDetailInlineFormSet
)
from .models import (
    Product, 
    Category,
    Combo
)

@login_required
def get_all_combos(request):
    
    combos = Combo.objects.all()
    ok = 0
    for combo in combos:
        for item in combo.products.all():
            if item.product.stock >= item.quantity:
                ok += 1
        
        if ok == len(combo.products.all()):
            combo.status = True
            combo.save()
        else:
            combo.status = False
            combo.save()

        ok = 0
        

    return render(request, 'inventory/combos.html', {
        'combos': Combo.objects.all()
    })

@login_required
def add_new_combo(request):
    if request.method == 'POST':
        form = NewComboForm(request.POST)

        if form.is_valid():
            new_combo = form.save(commit=False)
            formset = ComboDetailInlineFormSet(request.POST, instance=new_combo)

            if formset.is_valid():
                new_combo.save()
                formset.save()
                return HttpResponseRedirect(reverse('inventory:combos'))

    return render(request, 'inventory/combo-add.html', {
        'form': NewComboForm(),
        'formset': ComboDetailInlineFormSet()
    })

@login_required
def edit_combo(request, pk):
    combo = Combo.objects.get(pk=pk)

    # if is a post request
    if request.method == 'POST':
        form = NewComboForm(request.POST, instance=combo)

        if form.is_valid():
            formset = ComboDetailInlineFormSet(request.POST, instance=combo)
            
            if formset.is_valid():
                form.save()
                formset.save()

                return HttpResponseRedirect(reverse('inventory:combos'))
    # if is a get request
    return render(request, 'inventory/combo-edit.html', {
        'combo': combo,
        'form': NewComboForm(instance=combo),
        'formset': ComboDetailInlineFormSet(instance=combo)
    })

@login_required
def delete_combo(request, pk):
    combo = Combo.objects.get(pk=pk)
    
    if combo is not None:
        combo.delete()
        return HttpResponseRedirect(reverse('inventory:combos'))

@login_required
def get_combo_detail(request, pk):
    return render(request, 'inventory/combo-detail.html', {
        'combo': Combo.objects.get(pk=pk)
    })

@login_required
def get_all_products(request):
    return render(request, 'inventory/products.html', {
        'products': Product.objects.all()
    })

@login_required
def add_new_product(request):

    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)

        if form.is_valid():
            new_product = form.save()

            if new_product is not None:
                return HttpResponseRedirect(reverse('inventory:products'))
        else:
            return render(request, 'inventory/product-add.html', {
                'form': NewProductForm()
            })

    return render(request, 'inventory/product-add.html', {
        'form': NewProductForm()
    })

@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('inventory:products'))

    return render(request, 'inventory/product-edit.html', {
        'form': NewProductForm(instance=product),
        'product': product
    })

@login_required
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)

    if product is not None:
        product.delete()

        return HttpResponseRedirect(reverse('inventory:products'))

@login_required
def get_all_categories(request):
    return render(request, 'inventory/categories.html', {
        'categories': Category.objects.all()
    })

@login_required
def add_new_category(request):
    
    if request.method == 'POST':
        form = NewCategoryForm(request.POST)

        if form.is_valid():
            new_category = form.save()

            if new_category is not None:
                return HttpResponseRedirect(reverse('inventory:categories'))
        else:
            return render(request, 'inventory/category-add.html', {
                'form': NewCategoryForm()
            })

    return render (request, 'inventory/category-add.html', {
        'form': NewCategoryForm()
    })

@login_required
def delete_category(request, pk):
    category = Category.objects.get(pk=pk)

    if category is not None:
        category.delete()

        return HttpResponseRedirect(reverse('inventory:categories'))
