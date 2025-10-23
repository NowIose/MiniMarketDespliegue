from .models import Bitacora
from django.utils import timezone

def registrar_bitacora(usuario, request, descripcion):
    """
    Registra una acción en la bitácora con la IP del usuario y una descripción.
    """
    try:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

        Bitacora.objects.create(
            usuario=usuario,
            ip=ip,
            descripcion=descripcion,
            fecha=timezone.now()
        )
    except Exception as e:
        # Evita que errores de bitácora rompan otras funciones
        print(f"[Bitácora] Error registrando acción: {e}")