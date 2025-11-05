from django.urls import path
from . import views

urlpatterns = [
    # 🛒 Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/<str:accion>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/pago/', views.pago_qr, name='pago_qr'),
    # ✅ Rutas de cajero
    path("cajero/reservas/", views.cajero_reservas, name="cajero_reservas"),
    path("cajero/reservas/<int:reserva_id>/", views.cajero_reserva_detalle, name="cajero_reserva_detalle"),
    path("cajero/reservas/<int:reserva_id>/confirmar/", views.confirmar_reserva, name="confirmar_reserva"),

    path('mis_ventas/', views.mis_ventas, name='mis_ventas'),
path('detalle_venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
]
    # Otras rutas de Ventas pueden ir aquí