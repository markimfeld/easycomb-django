from django.urls import path

from . import views

app_name = 'suppliers'
urlpatterns = [
    path('', views.get_all_suppliers, name='suppliers'),
    path('new-supplier', views.add_new_supplier, name='new_supplier'),
    path('edit-supplier/<int:pk>', views.edit_supplier, name='edit-supplier'),
    path('delete/supplier/<int:pk>', views.delete_supplier, name='delete_supplier'),
    path('purchases', views.get_purchases, name='purchases'),
    path('delete/purchase/<int:pk>', views.delete_purchase, name='delete_purchase'),
    path('purchases/<int:pk>/detail', views.get_purchase_detail, name='purchase_detail'),
    path('new-purchase', views.add_new_purchase, name='new_purchase')
]