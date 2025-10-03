from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Producto

'''@login_required
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})'''
@login_required
def ver_productos(request):
    empleado = getattr(request.user, 'empleado', None)
    # Permitir si es empleado y ya completó (estado=True)
    if not empleado or not empleado.estado:
        messages.warning(request, "Debes completar tu registro de empleado para acceder a productos.")
        # Si tiene asignación pero incompleta, mandarlo a completar
        if empleado:
            return redirect('completar_empleado')
        return redirect('home')

    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})