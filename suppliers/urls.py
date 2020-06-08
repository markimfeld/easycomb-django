from django.urls import path

from . import views

app_name = 'suppliers'
urlpatterns = [
    path('', views.get_all_suppliers, name='suppliers'),
    path('purchases', views.get_purchases, name='purchases'),
    path('purchases/<int:pk>/detail', views.get_purchase_detail, name='purchase_detail'),
    path('new_purchase', views.new_purchase, name='new_purchase')
]