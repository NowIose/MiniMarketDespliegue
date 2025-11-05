from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.lista_proveedores, name='listar_proveedores'),
    path('proveedores/agregar/',views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:pk>', views.editar_proveedor, name= 'editar_proveedor'),
]