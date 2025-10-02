from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Bitacora
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or '0.0.0.0'

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    Bitacora.objects.create(usuario=user, ip=ip, descripcion='Inicio de sesión')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    # user puede ser None en logout en algunos flujos, chequea:
    if user:
        Bitacora.objects.create(usuario=user, ip=ip, descripcion='Cierre de sesión')