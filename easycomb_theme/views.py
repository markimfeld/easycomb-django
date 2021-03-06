from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Value as V, F, ExpressionWrapper, FloatField, IntegerField
from django.db.models.functions import Coalesce, Cast
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from clients.models import Customer
from inventory.models import Product, Combo
from orders.models import Order, Status, OrderDetail
from suppliers.models import PurchaseDetail, Purchase


def is_valid_params(params):
    return params is not None and params != ''

@login_required
def index(request):

    orders = Order.objects.all()
    order_details = OrderDetail.objects.all().select_related('combo', 'order')

    status = Status.objects.first()
    
    purchase_details = PurchaseDetail.objects.all().select_related('purchase') 

    # stock_stats = purchase_details \
    #    .annotate(total_percentages=Cast(((Cast(F('product__stock'), FloatField()) / Cast(F('quantity'), FloatField())) * 100.0), IntegerField())) \
    #    .values('product__name', 'product__stock', 'quantity', 'total_percentages') 


    # total cost for the last purchase in the same date
    total_cost = purchase_details.filter(purchase__date__exact='2020-6-29') \
        .annotate(subtotal_cost=ExpressionWrapper(F('quantity') * F('cost'), output_field=FloatField())) \
        .aggregate(total_cost=Sum('subtotal_cost'))

    # total_revenues = order_details.    
    revenue = OrderDetail.objects.exclude(combo=None) \
        .annotate(sub_total=ExpressionWrapper(F('price_combo') * F('quantity'), output_field=FloatField())) \
        .aggregate(total=Coalesce(Sum('sub_total'), V(0))) 

    # .filter(order__paid_status=True) \

    # total combos sold
    total_combos_sold = OrderDetail.objects.all().exclude(combo=None).aggregate(total=Coalesce(Sum('quantity'), V(0)))


    return render(request, 'easycomb_theme/index.html', {
        'revenue': revenue['total'],
        'products': Product.objects.all(),
        'orders': Order.objects.all(),
        'quantity_orders': Order.objects.filter(status=status).all().count,
        'quantity_products': Product.objects.all().count,
        'quantity_combos': Combo.objects.all().count,
        'quantity_customers': Customer.objects.filter(status=True).all().count,
        'total_combos_sold': total_combos_sold['total']
    })

@login_required
def get_total_combos(request, *args, **kwargs):

    order_details = OrderDetail.objects.all().select_related('combo', 'order')

    most_selled_combos = order_details.exclude(combo=None).values('combo__name', 'combo__price').annotate(total_sales=Coalesce(Sum('quantity'), V(0))).order_by('-total_sales')

    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')


    if (is_valid_params(startDate) and is_valid_params(endDate)):
        most_selled_combos = order_details.filter(order__date__gte=startDate, order__date__lte=endDate) \
        .exclude(combo=None).values('combo__name', 'combo__price').annotate(total_sales=Coalesce(Sum('quantity'), V(0))).order_by('-total_sales')

    status = Status.objects.first()

    labels = [item['combo__name'] for item in most_selled_combos]
    data = [item['total_sales'] for item in most_selled_combos]
    backgroundColor = ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de', '#1A7BFF', '#FCC108', '#5A6268', '#3773A6'] 
    donutData = {
        'labels': labels,
        'datasets': [
            {
                'data': data
                },
            ],
        'backgroundColor': backgroundColor
    }

    return JsonResponse(donutData)
