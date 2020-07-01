from django.urls import path

from . import views

app_name = 'easycomb_theme'
urlpatterns = [
    path('', views.index, name='index'),
    path('api/data/', views.get_total_combos, name="api_data"),
]
