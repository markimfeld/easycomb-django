from django.urls import path

from . import views

app_name = 'inventory'
urlpatterns = [
    path('combos', views.get_all_combos, name='combos'),
    path('new-combo', views.add_new_combo, name='new_combo'),
    path('combos/<int:pk>', views.get_combo_detail, name='combo_details'),
    path('edit-combo/<int:pk>', views.edit_combo, name='edit_combo'),
    path('delete/combo/<int:pk>', views.delete_combo, name='delete_combo'),
    path('products', views.get_all_products, name='products'),
    path('new-product', views.add_new_product, name='new_product'),
    path('delete/product/<int:pk>', views.delete_product, name="delete_product"),
    path('categories', views.get_all_categories, name="categories"),
    path('new-category', views.add_new_category, name='new_category'),
    path('delete/category/<int:pk>', views.delete_category, name="delete_category")
]