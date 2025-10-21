from django.urls import path
from . import views

urlpatterns = [
    path('categoria/', views.listar_categorias, name='listar_categorias'),
    path('categoria/<int:categoria_id>/', views.ver_categoria, name='ver_categoria'),
    path('categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('categoria/<int:categoria_id>/subcategoria/crear/', views.crear_subcategoria, name='crear_subcategoria'),
    path('categoria/<int:categoria_id>/producto/crear/', views.crear_producto, name='crear_producto'),
    path('', views.ver_productos, name='ver_productos'),
]