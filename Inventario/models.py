from django.db import models
from Productos.models import Producto
from Usuarios.models import Empleado
from django.utils import timezone

# Create your models here.

class Almacen(models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"


class Administra(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("empleado", "almacen")

    def __str__(self):
        return f"{self.empleado} administra {self.almacen}"


class Retiro(models.Model):
    fecha = models.DateField()

    def __str__(self):
        return f"Retiro {self.id} - {self.fecha}"


class DetalleRetiro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    retiro = models.ForeignKey(Retiro, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.CharField(max_length=100)

    class Meta:
        unique_together = ("producto", "retiro")

    def __str__(self):
        return f"{self.producto} retirado ({self.cantidad}) en {self.retiro}"


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre_empresa} ({self.correo})"


class Suministro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_ven = models.DateField()  # vencimiento
    fecha_com = models.DateField()  # compra
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_com = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField()

    def __str__(self):
        return f"Suministro {self.producto} de {self.proveedor} ({self.cantidad} unidades)"