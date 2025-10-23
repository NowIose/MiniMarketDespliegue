from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Productos.models import Producto
from .models import Carrito, ItemCarrito


## Agregar al carrito REVISAR IA
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # ✅ Obtiene o crea un carrito temporal para el usuario
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # ✅ Busca si el producto ya está en el carrito
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    if not creado:
        # Si ya existe, aumenta la cantidad
        item.cantidad += 1
        item.save()
        messages.info(request, f"🔼 Se aumentó la cantidad de '{producto.nombre}' en tu carrito.")
    else:
        messages.success(request, f"🛒 '{producto.nombre}' se agregó al carrito.")

    # ✅ Redirige a la página desde donde vino el usuario (sin salir)
    return redirect(request.META.get('HTTP_REFERER', 'listar_categorias'))

#VER CARRITO REVISAR IA
@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('producto')
    total = carrito.total()
    return render(request, 'ventas/ver_carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total
    })

#ACTUALIZAR CANTIDAD REVISAR IA
@login_required
def actualizar_cantidad(request, item_id, accion):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if accion == 'sumar':
        item.cantidad += 1
    elif accion == 'restar':
        if item.cantidad > 1:
            item.cantidad -= 1
        else:
            item.delete()
            messages.info(request, "Producto eliminado del carrito.")
            return redirect('ver_carrito')

    item.save()
    return redirect('ver_carrito')

#@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')

#@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.items.all().delete()
    messages.info(request, "Se vació tu carrito.")
    return redirect('ver_carrito')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from io import BytesIO
import qrcode, base64
from Usuarios.models import Cliente, Empleado, CargoLaboral
from Ventas.models import Carrito, DetalleVenta, MetodoPago, Venta
#from Notificaciones.models import Notificacion  # opcional si usas tabla Notificacion

@login_required
def pago_qr(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('producto')
    total = carrito.total()

    # Crear cliente si no existe
    cliente, creado = Cliente.objects.get_or_create(usuario=request.user)

    # Cajeros activos
    cargo_cajero = CargoLaboral.objects.filter(cargo__iexact="Cajero").first()
    cajeros = Empleado.objects.filter(estado=True, cargo=cargo_cajero)

    if request.method == "POST":
        id_cajero = request.POST.get("cajero")

        # ✅ Manejo de empleado según tipo de usuario
        try:
            empleado = Empleado.objects.get(usuario_id=request.user.id)
        except Empleado.DoesNotExist:
            empleado = Empleado.objects.get(usuario_id=id_cajero)

        # Generar QR
        datos_pago = f"Pago de {total} Bs. por {request.user.username} - Supermercado XYZ (Cajero: {empleado.usuario.username})"
        qr = qrcode.make(datos_pago)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Crear venta
        metodo_pago, _ = MetodoPago.objects.get_or_create(descripcion="Pago QR")

        venta = Venta.objects.create(
            id_cliente=cliente,
            id_empleado=empleado,
            id_pago=metodo_pago,
            descuento=0
        )

        for item in items:
            DetalleVenta.objects.create(
                id_venta=venta,
                id_producto=item.producto,
                cantidad=item.cantidad
            )

        carrito.items.all().delete()

        return render(request, "ventas/pago_qr.html", {
            "qr_base64": qr_base64,
            "total": total,
            "cajero": empleado,
            "nuevo_cliente": creado
        })

    # Vista GET
    return render(request, "ventas/seleccionar_cajero.html", {
        "cajeros": cajeros,
        "total": total
    })