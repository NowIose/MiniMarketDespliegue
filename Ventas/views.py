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
from Ventas.models import Carrito, DetalleVenta, MetodoPago, Venta,Reserva, DetalleReserva, Notificacion
#from Notificaciones.models import Notificacion  # opcional si usas tabla Notificacion

@login_required
def pago_qr(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('producto')
    total = carrito.total()

    cliente, creado = Cliente.objects.get_or_create(usuario=request.user)

    cargo_cajero = CargoLaboral.objects.filter(cargo__iexact="Cajero").first()
    cajeros = Empleado.objects.filter(estado=True, cargo=cargo_cajero)

    if request.method == "POST":
        id_cajero = request.POST.get("cajero")
        metodo = request.POST.get("metodo")

        empleado = Empleado.objects.get(usuario_id=id_cajero)

        # ✅ OPCIÓN 1: Reserva
        if metodo == "reserva":
            reserva = Reserva.objects.create(
                cliente=cliente,
                cajero=empleado,
                total=total,
            )
            Notificacion.objects.create(
                cajero=empleado,
                mensaje=f"Nuevo pedido de reserva del cliente {request.user.username}."
            )
            for item in items:
                DetalleReserva.objects.create(
                    reserva=reserva,
                    producto=item.producto,
                    cantidad=item.cantidad
                )

            carrito.items.all().delete()

            return render(request, "ventas/reserva_confirmada.html", {
                "reserva": reserva,
                "cajero": empleado,
                "total": total
            })

        # ✅ OPCIÓN 2: Pago QR (sin cambios)
        datos_pago = f"Pago de {total} Bs. por {request.user.username} - Supermercado XYZ (Cajero: {empleado.usuario.username})"
        qr = qrcode.make(datos_pago)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

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

    return render(request, "ventas/seleccionar_cajero.html", {
        "cajeros": cajeros,
        "total": total
    })

from django.utils.timezone import localdate


@login_required
def cajero_reservas(request):
    # Verificar que es empleado
    try:
        cajero = request.user.empleado
    except Empleado.DoesNotExist:
        messages.error(request, "No eres empleado.")
        return redirect("home")

    # Verificar que sea cajero
    if cajero.cargo.cargo != "Cajero":
        messages.error(request, "No eres cajero.")
        return redirect("home")

    # Fecha de hoy
    hoy = localdate()

    # Todas las reservas del cajero de hoy
    reservas_hoy = Reserva.objects.filter(
        cajero=cajero,
        fecha__date=hoy
    ).order_by("-fecha")

    # Separarlas por estado
    pendientes = reservas_hoy.filter(estado="Pendiente")
    confirmadas = reservas_hoy.filter(estado="Confirmada")

    return render(request, "ventas/cajero_reservas.html", {
        "pendientes": pendientes,
        "confirmadas": confirmadas,
    })

@login_required
def cajero_reserva_detalle(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    try:
        cajero = request.user.empleado
    except Empleado.DoesNotExist:
        messages.error(request, "No eres empleado.")
        return redirect("home")

    # ✅ Seguridad: un cajero solo ve sus reservas
    if reserva.cajero != cajero:
        messages.error(request, "No tienes permiso para ver esta reserva.")
        return redirect("cajero_reservas")

    detalles = reserva.detalles.select_related("producto")

    return render(request, "ventas/cajero_reserva_detalle.html", {
        "reserva": reserva,
        "detalles": detalles
    })

@login_required
def confirmar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    try:
        cajero = request.user.empleado
    except Empleado.DoesNotExist:
        messages.error(request, "No eres empleado.")
        return redirect("home")

    if reserva.cajero != cajero:
        messages.error(request, "No tienes permiso para confirmar esta reserva.")
        return redirect("cajero_reservas")

    if reserva.estado != "Pendiente":
        messages.warning(request, "La reserva ya fue procesada.")
        return redirect("cajero_reservas")

    # ✅ Crear venta
    metodo_pago, _ = MetodoPago.objects.get_or_create(descripcion="Reserva Confirmada")

    venta = Venta.objects.create(
        id_cliente=reserva.cliente,
        id_empleado=cajero,
        id_pago=metodo_pago,
        descuento=0,
        reserva=reserva  # 🔥 vincula la reserva con la venta
    )

    # ✅ Crear detalle de venta
    for det in reserva.detalles.all():
        DetalleVenta.objects.create(
            id_venta=venta,
            id_producto=det.producto,
            cantidad=det.cantidad
        )

    # ✅ Cambiar estado
    reserva.estado = "Confirmada"
    reserva.save()

    messages.success(request, f"Reserva #{reserva.id} confirmada correctamente.")
    return redirect("cajero_reservas")

@login_required
def mis_ventas(request):
    try:
        cliente = request.user.cliente
    except:
        messages.error(request, "No eres cliente.")
        return redirect("home")

    ventas = Venta.objects.filter(id_cliente=cliente).select_related('reserva').order_by('-fecha')

    return render(request, "ventas/mis_ventas.html", {"ventas": ventas})

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id, id_cliente__usuario=request.user)
    detalles = venta.detalleventa_set.select_related('id_producto')
    return render(request, "ventas/detalle_venta.html", {
        "venta": venta,
        "detalles": detalles
    })