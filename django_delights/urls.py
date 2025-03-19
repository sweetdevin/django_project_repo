from django.contrib.auth import views as user_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu_view.as_view(), name='menu'),
    path('menu/add', views.Menu_item_create_view.as_view(), name='menu_add'),
    path('inventory/', views.ingredient_view.as_view(), name='inventory'),
    path('inventory/add', views.InventoryCreateUpdateView.as_view(), name='inventory_add'),
    path('login/', user_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('menu/<pk>/', views.Menu_detail_view.as_view(), name='menu_detail'),
    path('menu/<pk>/add', views.recipe_item_createview.as_view(), name='recipe_item_add')
]