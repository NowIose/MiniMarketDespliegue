from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('retiros/', views.lista_retiros, name='lista_retiros'),
    path('retiros/nuevo/', views.nuevo_retiro, name='nuevo_retiro'),
]
