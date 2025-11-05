"""URL para la aplicacion de Reportes"""
from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel_reportes, name='panel_reportes'),
    path('reporte_ventas/', views.reporte_ventas, name='reporte_ventas')
]
