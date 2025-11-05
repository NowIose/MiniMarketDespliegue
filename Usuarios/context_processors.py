from Ventas.models import Notificacion
from Usuarios.models import Empleado

def notificaciones_cajero(request):
    if not request.user.is_authenticated:
        return {}

    try:
        empleado = request.user.empleado
    except Empleado.DoesNotExist:
        return {}

    # Solo mostrar para cajeros
    if empleado.cargo.cargo != "Cajero":
        return {}

    # Contar las NO leídas
    count = empleado.notificaciones.filter(leido=False).count()

    return {
        "notificaciones_cajero": count
    }