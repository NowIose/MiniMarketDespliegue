"""
WSGI config for Central project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Central.settings')


# 🚀 Bloque temporal para crear superusuario en Render
if os.environ.get("CREATE_SUPERUSER") == "True":
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("✅ Superusuario 'admin' creado con éxito.")

application = get_wsgi_application()
