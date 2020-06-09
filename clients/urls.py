from django.urls import path

# ---------------------------------
from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.get_all_clients, name='customers'),
    path('new-customer', views.add_new_customer, name='new_customer'),
    path('edit-customer/<int:pk>', views.edit_customer, name='edit_customer'),
    path('delete/customer/<int:pk>', views.delete_customer, name='delete_customer')
]