from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu_view.as_view(), name='menu'),
    path('menu/add', views.Menu_item_create_view.as_view(), name='menu_add'),
    path('inventory/', views.ingredient_view.as_view(), name='inventory'),
    path('inventory/add', views.InventoryCreateUpdateView.as_view(), name='inventory_add'),
]