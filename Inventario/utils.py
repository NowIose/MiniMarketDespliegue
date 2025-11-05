from datetime import date
from .models import DetalleSuministro, Retiro, DetalleRetiro

def generar_retiros_automaticos():
    hoy = date.today()
    # ✅ Buscar productos vencidos en los detalles del suministro
    detalles_vencidos = DetalleSuministro.objects.filter(fecha_ven__lte=hoy, estado=True)

    if not detalles_vencidos.exists():
        return None

    # ✅ Crear retiro automático (sin empleado)
    retiro_auto = Retiro.objects.create(tipo=Retiro.AUTOMATICO)

    for detalle in detalles_vencidos:
        # Registrar detalle del retiro
        DetalleRetiro.objects.create(
            producto=detalle.producto,
            retiro=retiro_auto,
            cantidad=detalle.cantidad,
            motivo=f"Producto vencido ({detalle.fecha_ven})"
        )

        # 🔧 Actualizar el stock del producto
        detalle.producto.cantidad -= detalle.cantidad
        detalle.producto.save()

        # Marcar este detalle de suministro como inactivo
        detalle.estado = False
        detalle.save()

    return retiro_auto