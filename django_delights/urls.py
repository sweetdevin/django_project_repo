from django.contrib.auth import views as user_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu_view.as_view(), name='menu'),
    path('menu/add', views.Menu_item_create_view.as_view(), name='menu_add'),
    path('inventory/', views.ingredient_view.as_view(), name='inventory'),
    path('inventory/add', views.InventoryCreateUpdateView.as_view(), name='inventory_add'),
    path('login/', views.custom_loginview.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
    path('menu/<pk>/', views.Menu_detail_view.as_view(), name='menu_detail'),
    path('menu/<pk>/add', views.recipe_item_createview.as_view(), name='recipe_item_add'),
    path('menu/<pk>/update', views.Menu_item_update_view.as_view(), name='menu_update'),
    path('menu/<pk>/delete', views.Menu_item_delete_view.as_view(), name='menu_delete'),
    path('menu/<pk>/review', views.review_createview.as_view(), name='review_create'),
    path('review/<pk>/update', views.review_updateview.as_view(), name='review_update'),
    path('review/<pk>/delete', views.review_delete_view.as_view(), name = 'review_delete'),
    path('purchases/', views.purchase_view.as_view(), name='purchase_view'),
    path('recipe/<pk>/update', views.recipe_update_view.as_view(), name='recipe_update'),
    path('recipe/<pk>/delete', views.recipe_delete_view.as_view(), name='recipe_delete'),
    path('inventory/<pk>/delete', views.inventory_deleteview.as_view(), name='inventory_delete'),
    path('purchases/<pk>/update', views.purchase_update_view.as_view(), name='purchase_update'),
    path('purchase/<pk>/delete', views.purchase_delete_view.as_view(), name='purchase_delete'),
]