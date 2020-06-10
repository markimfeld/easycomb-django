from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.get_all_orders, name='orders'),
    path('<int:pk>/details', views.get_order_details, name='order_details'),
    path('new-order', views.add_new_order, name='new_order'),
]