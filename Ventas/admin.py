from django.contrib import admin
from Ventas.models import MetodoPago, Venta, DetalleVenta, Devolucion, DetalleDevolucion

# Register your models here.
admin.site.register(MetodoPago)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Devolucion)
admin.site.register(DetalleDevolucion)
