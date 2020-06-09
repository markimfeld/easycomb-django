from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.get_all_orders, name='orders')
]