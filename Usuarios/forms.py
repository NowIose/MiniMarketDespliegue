from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Empleado

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'correo', 'telefono', 'password1', 'password2', 'te', 'tc']
# Usuarios/forms.p

'''class AsignarEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cargo', 'sueldo'] 

from django import forms
from .models import Empleado'''
class AsignarEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cargo', 'sueldo']  # agregar sueldo
        widgets = {
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'sueldo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class EmpleadoRegistroForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['ci', 'sexo', 'direccion']  # Solo lo que el empleado completa