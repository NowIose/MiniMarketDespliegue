from django.db import models
from Usuarios.models import Cliente, Empleado
from Productos.models import Producto
# Create your models here.

class MetodoPago(models.Model):
    descripcion=models.CharField(max_length=50)


    def __str__(self):
     return self.descripcion

class Venta(models.Model):
   fecha=models.DateField(auto_now_add=True) #guarda automaticamente la fecha
   descuento=models.DecimalField(max_digits=5, decimal_places=2,default=0)
   id_cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,null=False,related_name="ventas")
   id_empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE,null=False,related_name="ventas")
   id_pago=models.ForeignKey(MetodoPago,on_delete=models.CASCADE,null=False,related_name="ventas")

   @property
   def total_venta(self):
       subtotal=sum(d.cantidad * d.precio for d in self.detalleventa_Set.all())
       monto_descuento=subtotal * (self.descuento / 100)
       return subtotal-monto_descuento
   
   def __str__(self):
       return f"{self.id_cliente.nombre} {self.fecha.strftime('%Y-%m-%d')}"
   
class DetalleVenta(models.Model):
    id_venta=models.ForeignKey(Venta,on_delete=models.CASCADE,null=False)
    id_producto=models.ForeignKey(Producto,on_delete=models.CASCADE,null=False)
    cantidad=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
     unique_together = ('id_venta', 'id_producto')

    def __str__(self):
        return self.id_producto.nombre + " - " + str(self.cantidad) + " unidades"

    

class Devolucion(models.Model):
    fecha=models.DateField(auto_now_add=True)

    def __str__(self):
       return f"Devolucion {self.id} - {self.fecha.strftime('%Y-%m-%d')}"
    
class DetalleDevolucion(models.Model):
   id_devolucion=models.ForeignKey(Devolucion,on_delete=models.CASCADE,null=False)
   id_detalle_venta=models.ForeignKey(DetalleVenta,on_delete=models.CASCADE,null=False)
   cantidad=models.DecimalField(max_digits=10,decimal_places=2)
   motivo=models.TextField()

   class Meta:
       unique_together = ('id_devolucion', 'id_detalle_venta')

   def __str__(self):
      return f"{self.id_detalle_venta.id_producto.nombre} - {self.cantidad} unidades"

