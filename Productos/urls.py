from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_productos, name='ver_productos'),
]