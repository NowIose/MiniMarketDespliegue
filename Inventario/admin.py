from django.contrib import admin
from Inventario.models import Almacen, Administra, Retiro, DetalleRetiro, Proveedor, Suministro
# Register your models here.

admin.site.register(Almacen)
admin.site.register(Administra)
admin.site.register(Retiro)
admin.site.register(DetalleRetiro)
admin.site.register(Proveedor)
admin.site.register(Suministro)
