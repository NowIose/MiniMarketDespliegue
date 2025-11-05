from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Retiro, DetalleRetiro, Producto
from Usuarios.models import Empleado
from django.utils import timezone
from decimal import Decimal
from .utils import generar_retiros_automaticos
@login_required
def nuevo_retiro(request):
    empleado = Empleado.objects.get(usuario=request.user)

    # Solo los gerentes pueden realizar retiros manuales
    if empleado.cargo.cargo != "Gerente":
        messages.error(request, "Solo los gerentes pueden realizar retiros manuales.")
        return redirect('inventario:lista_retiros')

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = Decimal(request.POST.get('cantidad'))  # 👈 aquí usamos Decimal
        motivo = request.POST.get('motivo')

        producto = Producto.objects.get(id=producto_id)

        if cantidad > producto.cantidad:
            messages.error(request, "No hay suficiente stock disponible.")
            return redirect('inventario:nuevo_retiro')

        retiro = Retiro.objects.create(
            empleado=empleado,
            tipo=Retiro.MANUAL,
            fecha=timezone.now()
        )

        DetalleRetiro.objects.create(
            producto=producto,
            retiro=retiro,
            cantidad=cantidad,
            motivo=motivo
        )

        # 🔧 Usamos Decimal para evitar errores de tipo
        producto.cantidad -= cantidad
        producto.save()

        messages.success(request, "✅ Retiro realizado con éxito.")
        return redirect('inventario:lista_retiros')

    productos = Producto.objects.all()
    return render(request, 'retiros/nuevo_retiro.html', {'productos': productos})


@login_required
def lista_retiros(request):

    generar_retiros_automaticos()
    retiros = Retiro.objects.order_by('-fecha')[:10]
    return render(request, 'retiros/lista_retiros.html', {'retiros': retiros})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Proveedor
from .forms import ProveedorForm


def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedores/listar_proveedores.html', {'proveedores':proveedores})

def agregar_proveedor(request):
    if request.method =='POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario:listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/agregar_proveedor.html', {'form':form})

def editar_proveedor(request, pk):
    proveedor= get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('inventario:listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar_proveedor.html', {'form':form})