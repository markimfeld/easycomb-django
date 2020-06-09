from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

# Create your views here.
from .forms import ( 
    NewProductForm,
    NewCategoryForm
)
from .models import (
    Product, 
    Category,
    Combo
)

def get_all_combos(request):
    return render(request, 'inventory/combos.html', {
        'combos': Combo.objects.all()
    })

def get_combo_detail(request, pk):
    return render(request, 'inventory/combo-detail.html', {
        'combo': Combo.objects.get(pk=pk)
    })

def get_all_products(request):
    return render(request, 'inventory/products.html', {
        'products': Product.objects.all()
    })

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


def delete_product(request, pk):
    product = Product.objects.get(pk=pk)

    if product is not None:
        product.delete()

        return HttpResponseRedirect(reverse('inventory:products'))


def get_all_categories(request):
    return render(request, 'inventory/categories.html', {
        'categories': Category.objects.all()
    })


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

def delete_category(request, pk):
    category = Category.objects.get(pk=pk)

    if category is not None:
        category.delete()

        return HttpResponseRedirect(reverse('inventory:categories'))