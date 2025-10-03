from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
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

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Correo", max_length=254)

    def get_users(self, email):
        """
        Buscar usuarios activos por 'correo' en lugar de 'email'.
        """
        active_users = Usuario._default_manager.filter(correo__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())
'''class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Correo", max_length=254)

    def get_users(self, email):
        email_field = Usuario._meta.get_field('correo')
        active_users = Usuario._default_manager.filter(**{
        f'{email_field.name}__iexact': email,
        'is_active': True,
    })
        print("Usuarios encontrados:", list(active_users))  # <-- depuración
        return (u for u in active_users if u.has_usable_password())
'''