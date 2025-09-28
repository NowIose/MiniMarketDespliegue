from django.contrib import admin
from Productos.models import Categoria, Producto
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)