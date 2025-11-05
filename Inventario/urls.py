from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('retiros/', views.lista_retiros, name='lista_retiros'),
    path('retiros/nuevo/', views.nuevo_retiro, name='nuevo_retiro'),
    path('proveedores/', views.lista_proveedores, name='listar_proveedores'),
    path('proveedores/agregar/',views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:pk>', views.editar_proveedor, name= 'editar_proveedor'),
    path('suministros/nuevo/', views.nuevo_suministro, name='nuevo_suministro'),
    path('suministros/', views.lista_suministros, name='lista_suministros'),
]