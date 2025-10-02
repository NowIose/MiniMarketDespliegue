from django.apps import AppConfig

'''
class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios'
'''
class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios'

    def ready(self):
        # importa señales para que se enlacen los receivers
        import Usuarios.signals  # NO cambiar: importa para registrar handlers