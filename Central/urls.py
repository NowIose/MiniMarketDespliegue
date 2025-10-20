"""
URL configuration for Central project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from Usuarios import views as usuario_views
from Productos import views as producto_views

urlpatterns = [
    path('', usuario_views.login_view, name='home'),  # 👈 raíz muestra el login
    path('admin/', admin.site.urls),
    path('home/', usuario_views.home, name='home'),
    path('usuarios/', include('Usuarios.urls')),
    path('productos/', include('Productos.urls')),
    path('categorias/', producto_views.listar_categorias, name='listar_categorias'),
]
