from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ObjectDoesNotExist #capturar error si no existe el objeto

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, null=False)
    correo = models.EmailField(unique=True, null=False)
    te = models.BooleanField(default=False)  # términos empresa
    tc = models.BooleanField(default=False)  # términos condiciones

    # USERNAME_FIELD = 'username'  # Por defecto en AbstractUser es 'username'
    # REQUIRED_FIELDS = []         # Por defecto vacío

    """
    Campos heredados por defecto desde AbstractUser:
    - username        : CharField, max_length=150, único (identificador por defecto)
    - first_name      : CharField, max_length=150
    - last_name       : CharField, max_length=150
    - email           : EmailField
    - password        : CharField, max_length=128
    - is_staff        : BooleanField (permiso de admin)
    - is_active       : BooleanField (usuario activo)
    - is_superuser    : BooleanField (permiso total)
    - last_login      : DateTimeField
    - date_joined     : DateTimeField
    """
    def __str__(self):
        return f"{self.username} ({self.correo})"
    @property
    def es_gerente(self):
        """
        True si el usuario tiene un Empleado asociado cuyo cargo es 'Gerente'.
        Evita errores si no existe el objeto Empleado.
        """
        try:
            return self.empleado.cargo.cargo == "Gerente"
        except ObjectDoesNotExist:
            return False

####CLIENTE
    
class Cliente(models.Model):
    usuario=models.OneToOneField(Usuario, on_delete=models.PROTECT,primary_key=True)
    #Cliente puede tener campos en otras tablas uso Protect para si tiene realcion con otra tabla no lo borre

    def __str__(self):
        return f"{self.usuario.username} ({self.usuario.correo})"
    
#####CARGO LABORAL
class CargoLaboral(models.Model):
    cargo=models.CharField(max_length=50,unique=True)
    descripcion=models.TextField()  
    def __str__(self):
        return self.cargo

#####EMPLEADO  
'''class Empleado(models.Model):
    usuario=models.OneToOneField(Usuario, on_delete=models.PROTECT,primary_key=True)
    ci=models.IntegerField(unique=True)
    sexo=models.CharField(max_length=1)
    direccion=models.CharField(max_length=100)
    fecha_contratacion=models.DateField()
    sueldo=models.DecimalField(max_digits=10, decimal_places=2)
    estado=models.BooleanField()
    cargo=models.ForeignKey(CargoLaboral,on_delete=models.PROTECT)

    def __str__(self):
        return (
            f"Usuario: {self.usuario.username}, "
            f"CI: {self.ci}, "
            f"Sexo: {self.sexo}, "
            f"Dirección: {self.direccion}, "
            f"Fecha Contratación: {self.fecha_contratacion}, "
            f"Sueldo: {self.sueldo}, "
            f"Estado: {self.estado}, "
            f"Cargo: {self.cargo.cargo}"
        )'''
# Usuarios/models.py (solo la clase Empleado)
'''class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT, primary_key=True)
    ci = models.IntegerField(unique=True, null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    fecha_contratacion = models.DateField(null=True, blank=True)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.BooleanField(default=False)  # False = aún no completó registro
    cargo = models.ForeignKey(CargoLaboral, on_delete=models.PROTECT)

    def __str__(self):
        # manejar valores None para que no explote el __str__
        ci = self.ci or "N/A"
        sexo = self.sexo or "-"
        direccion = self.direccion or "-"
        fecha = self.fecha_contratacion or "-"
        sueldo = self.sueldo or 0
        cargo_nombre = self.cargo.cargo if self.cargo else "-"
        return (
            f"Usuario: {self.usuario.username}, "
            f"CI: {ci}, "
            f"Sexo: {sexo}, "
            f"Dirección: {direccion}, "
            f"Fecha Contratación: {fecha}, "
            f"Sueldo: {sueldo}, "
            f"Estado: {self.estado}, "
            f"Cargo: {cargo_nombre}"
        )'''
class Empleado(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT, primary_key=True)
    ci = models.IntegerField(unique=True, null=True, blank=True)  # empleado
    sexo = models.CharField(max_length=1, null=True, blank=True)  # empleado
    direccion = models.CharField(max_length=100, null=True, blank=True)  # empleado
    
    fecha_contratacion = models.DateField(null=True, blank=True)  # se pondrá al completar registro
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)  # gerente
    
    estado = models.BooleanField(default=False)
    cargo = models.ForeignKey(CargoLaboral, on_delete=models.PROTECT)

    def __str__(self):
        return (
            f"Usuario: {self.usuario.username}, "
            f"CI: {self.ci}, "
            f"Sexo: {self.sexo}, "
            f"Dirección: {self.direccion}, "
            f"Fecha Contratación: {self.fecha_contratacion}, "
            f"Sueldo: {self.sueldo}, "
            f"Estado: {self.estado}, "
            f"Cargo: {self.cargo.cargo}"
        )
class Bitacora(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=False)
    ip = models.CharField(max_length=45,null=False)  # Soporta IPv6
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    descripcion = models.CharField(max_length=100,null=False)

    def __str__(self):
        return f"Bitácora: {self.usuario.username} - {self.fecha} - {self.descripcion}"
    
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Usuario)
def set_email_from_correo(sender, instance, **kwargs):
    if instance.correo and not instance.email:
        instance.email = instance.correo