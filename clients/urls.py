from django.urls import path

# ---------------------------------
from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.get_all_clients, name='customers'),
    path('edit-customer/<int:pk>', views.edit_customer, name='edit-customer'),
    path('delete/customer/<int:pk>', views.delete_customer, name='delete_customer')
]