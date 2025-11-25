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
    

    path("cajero/reservas/", views.cajero_reservas, name="cajero_reservas"),
    path("cajero/reservas/<int:reserva_id>/", views.cajero_reserva_detalle, name="cajero_reserva_detalle"),
    path("cajero/reservas/<int:reserva_id>/confirmar/", views.confirmar_reserva, name="confirmar_reserva"),
    path('venta/<int:venta_id>/entregado/', views.marcar_entregado, name='marcar_entregado'),

    path('mis_ventas/', views.mis_ventas, name='mis_ventas'),
    path('detalle_venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    # ... otras rutas ...
    path('paypal/iniciar/', views.iniciar_pago_paypal, name='iniciar_pago_paypal'),
    path('paypal/success/', views.paypal_success, name='paypal_success'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),

    path('carrito/pago-qr-interoperable/', views.pago_qr_interoperable, name='pago_qr_interoperable'),
    path('carrito/qr-pdf/', views.descargar_pdf_qr, name='descargar_pdf_qr'),
    path('webhook/payments/', views.webhook_pago_psp, name='webhook_pago_psp'),
    path("ventas/pago_union/", views.pago_union, name="pago_union"),
    path("ventas/pago_union/confirmar/", views.confirmar_pago_union, name="confirmar_pago_union"),

    path("ventas/cajero/", views.ventas_cajero, name="ventas_cajero")
]
    # Otras rutas de Ventas pueden ir aquí