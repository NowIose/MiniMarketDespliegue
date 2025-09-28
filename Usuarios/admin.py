from django.contrib import admin
from .models import Usuario, Cliente, CargoLaboral, Empleado, Bitacora

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(CargoLaboral)
admin.site.register(Empleado)
admin.site.register(Bitacora)