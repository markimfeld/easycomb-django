from django.urls import path

from . import views

app_name = 'easycomb_theme'
urlpatterns = [
    path('', views.index, name='index')
]