## las apps no tienen archivo urls.py por defecto, hay que crearlo
##luego incluirlo en el urls.py del proyecto principal Central/urls.py

from django.urls import path
from Usuarios import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('empleados/', views.ver_empleados, name='ver_empleados'),
    path('bitacora/', views.ver_bitacora, name='ver_bitacora'),
    path('asignar_empleado/<int:usuario_id>/', views.asignar_empleado, name='asignar_empleado'),
    path('completar_empleado/', views.completar_registro_empleado, name='completar_empleado'),
]
