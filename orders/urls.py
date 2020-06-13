from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.get_all_orders, name='orders'),
    path('change_status/<int:pk>', views.change_status_order, name='change_status_order'),
    path('details/<int:pk>', views.get_order_details, name='order_details'),
    path('register_paid/<int:pk>', views.register_order_paid, name='register_order_paid'),
    path('new-order', views.add_new_order, name='new_order'),
    path('delete/<int:pk>', views.delete_order, name='delete_order')
]