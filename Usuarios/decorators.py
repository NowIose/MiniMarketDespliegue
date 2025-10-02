##BUENA PRACTICA: Decoradores para vistas basados en cargos de empleados. 
##asi se protege mejor las vistas que solo con @login_required
##Ejemplo de uso: @cargo_requerido('Gerente') o @cargo_requerido('Gerente','Administrador')
##Si no autenticado redirige a 'login', si no tiene cargo permitido redirige a 'home'.
##Este no es propio de Django lo crea el desarrollador

from functools import wraps
from django.shortcuts import redirect
from .models import Empleado

def cargo_requerido(*cargos_permitidos):
    """
    Usa: @cargo_requerido('Gerente') o @cargo_requerido('Gerente','Administrador')
    Redirige a 'login' si no autenticado, a 'home' si no tiene cargo permitido.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                empleado = Empleado.objects.get(usuario=request.user)
            except Empleado.DoesNotExist:
                return redirect('home')
            if empleado.cargo.cargo not in cargos_permitidos:
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator