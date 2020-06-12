from django.urls import path

# ---------------------------------
from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.get_all_clients, name='customers'),
    path('details/<int:pk>', views.get_customer_details, name='customer_details'),
    path('new-customer', views.add_new_customer, name='new_customer'),
    path('edit-customer/<int:pk>', views.edit_customer, name='edit_customer'),
    path('activate/customer/<int:pk>', views.activate_customer, name='activate_customer'),
    path('deactivate/customer/<int:pk>', views.deactivate_customer, name='deactivate_customer')
]