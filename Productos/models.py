from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50,null=False)
    categoria_padre = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='subcategorias')

    def __str__(self):
        padre_id = self.categoria_padre.id if self.categoria_padre else None
        return f"ID: {self.id} | Nombre: {self.nombre} | Padre ID: {padre_id}"


class Producto(models.Model):
    nombre=models.CharField(max_length=50,null=False)
    cantidad=models.DecimalField(max_digits=10, decimal_places=2,null=False)
    unidad_medida=models.CharField(max_length=20,null=False)
    precio_venta=models.DecimalField(max_digits=10, decimal_places=2,null=False)
    categoria=models.ForeignKey(Categoria,on_delete=models.PROTECT)  
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)    # Nueva línea para la imagen del producto

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Cantidad: {self.cantidad} {self.unidad_medida} | Precio Venta: {self.precio_venta} | Categoria: {self.categoria.nombre}"   