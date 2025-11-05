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


from .models import Proveedor, Producto, Suministro, DetalleSuministro
from Usuarios.models import Empleado
@login_required
def nuevo_retiro(request):
    empleado = Empleado.objects.get(usuario=request.user)

    # Solo el Gerente o Encargado de Suministros pueden hacer retiros manuales
    if empleado.cargo.cargo not in ["Gerente", "Encargado de Suministros"]:
        messages.error(request, "Solo el Gerente o el Encargado de Suministros pueden realizar retiros manuales.")
        return redirect('inventario:lista_retiros')

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = Decimal(request.POST.get('cantidad'))
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

from django.http import HttpResponse

@login_required
def nuevo_suministro(request):
    empleado = Empleado.objects.get(usuario=request.user)

    # Solo el Gerente o el Encargado de Suministros pueden registrar suministros
    if empleado.cargo.cargo not in ["Gerente", "Encargado de Suministros"]:
        messages.error(request, "No tienes permiso para registrar suministros.")
        return redirect('listar_categorias')

    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        fecha_com = request.POST.get('fecha_com')
        productos_ids = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio_com')
        fechas_ven = request.POST.getlist('fecha_ven')

        # Validación básica
        if not proveedor_id or not productos_ids:
            messages.error(request, "Debe seleccionar un proveedor y al menos un producto.")
            return redirect('inventario:nuevo_suministro')

        proveedor = Proveedor.objects.get(id=proveedor_id)
        suministro = Suministro.objects.create(
            proveedor=proveedor,
            empleado=empleado,
            fecha_com=fecha_com if fecha_com else timezone.now().date()
        )

        total = Decimal('0.00')

        for i in range(len(productos_ids)):
            producto = Producto.objects.get(id=productos_ids[i])
            cantidad = Decimal(cantidades[i])
            precio = Decimal(precios[i])
            fecha_ven = fechas_ven[i]

            # Crear el detalle (el modelo se encarga de actualizar el stock)
            DetalleSuministro.objects.create(
                suministro=suministro,
                producto=producto,
                cantidad=cantidad,
                precio_com=precio,
                fecha_ven=fecha_ven,
                estado=True
            )

            total += cantidad * precio

        # Guardar total del suministro
        suministro.total_com = total
        suministro.save()

        messages.success(request, f"✅ Suministro registrado correctamente. Total: {total} Bs.")
        return redirect('listar_categorias')

    return render(request, 'suministros/nuevo_suministro.html', {
        'proveedores': proveedores,
        'productos': productos,
        'fecha_hoy': timezone.now().date(),
    })

@login_required
def lista_suministros(request):
    """
    Muestra todos los suministros registrados con sus detalles.
    Solo visible para Gerente y Encargado de Suministros.
    """
    empleado = Empleado.objects.get(usuario=request.user)

    if empleado.cargo.cargo not in ["Gerente", "Encargado de Suministros"]:
        messages.error(request, "No tienes permiso para ver los suministros.")
        return redirect('listar_categorias')

    suministros = Suministro.objects.prefetch_related('detalles', 'proveedor', 'empleado').order_by('-fecha_com')

    return render(request, 'suministros/lista_suministros.html', {'suministros': suministros})
