from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:seleccion_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
]
