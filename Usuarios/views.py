from django.shortcuts import render,redirect
from Usuarios.models import Usuario,Cliente,Empleado,CargoLaboral,Bitacora
from django.http import JsonResponse, HttpResponse # Import HttpResponse if needed
from django.contrib.auth.forms import UserCreationForm #Crea el formulario de registro

from django.contrib.auth import login, authenticate, logout # Django nos proporciona login logout  y autenticacion
from django.contrib.auth.forms import AuthenticationForm  #auntenticacion
from .forms import CustomUserCreationForm                 #importamos de forms.py




from .forms import CustomUserCreationForm #Importa el formulario personalizado esto de forms.py

# Create your views here.

#PRUEBA DE CONEXION A LA BASE DE DATOS
def getUsuarios(request):  #esta vista devuelve todos los usuarios en formato JSON
    Usuario1 = list(Usuario.objects.values())
    return JsonResponse(Usuario1, safe=False)
def getUsuarioById(request, id):    #esta vista devuelve un usuario por su ID en formato JSON
    try:
        usuario = Usuario.objects.filter(id=id).values().first()
        if usuario:
            return JsonResponse(usuario, safe=False)
        else:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def hello(request,username):
    return HttpResponse(f"<h2>Hello World {username}</h2>") 
   # return HttpResponse("<h2>Hello World %s </h2>"%username)  forma antigua de concatenar 

##LOGEO DE USUARIOS

'''def home(request): #ANTIGUA VERSION
    return render(request, 'home.html')
'''
from django.contrib.auth.decorators import login_required
from django.contrib import messages #importa mensajes para notificaciones

def home(request):
    # Verifica si el usuario tiene un registro de Empleado y está incompleto
    if hasattr(request.user, 'empleado') and not request.user.empleado.estado:
        messages.info(request, "Fuiste asignado como empleado, por favor completa tus datos.")
    return render(request, 'home.html')


'''def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente después de registrarse
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
'''
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print('entrar login')
            user = form.get_user()
            login(request, user)
            return redirect('home')   # 👈 esto debería mandarte a home
    else:
        print('no entro login')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Commit=False para poder ver el objeto antes de guardar
            user = form.save(commit=False)

            # Debug: imprimir en consola los datos del usuario
            print("===== DEBUG SIGNUP =====")
            print("Username:", user.username)
            print("Correo:", user.correo)
            print("Telefono:", user.telefono)
            print("is_active:", user.is_active)

            # Asegurarnos que el usuario esté activo
            user.is_active = True
            user.save()  # Guardamos en la base

            # Debug: Confirmar que se guardó
            print("Usuario guardado con ID:", user.id)

            login(request, user)  # inicia sesión automáticamente
            messages.success(request, f"Usuario {user.username} creado y logueado!")
            return redirect('home')
        else:
            # Debug: mostrar errores del formulario
            print("===== DEBUG ERRORES =====")
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .decorators import cargo_requerido

@login_required
@cargo_requerido("Gerente")
def ver_clientes(request):
    clientes = Cliente.objects.select_related('usuario').all()
    return render(request, 'clientes.html', {'clientes': clientes})

'''@login_required
@cargo_requerido("Gerente")
def ver_empleados(request):
    empleados = Empleado.objects.select_related('usuario', 'cargo').all()
    return render(request, 'empleados.html', {'empleados': empleados})'''
@login_required
@cargo_requerido("Gerente")
def ver_empleados(request):
    # Lista de empleados ya creados
    empleados = Empleado.objects.select_related('usuario', 'cargo').all()
    
    # Usuarios que aún no son empleados
    usuarios_pendientes = Usuario.objects.exclude(empleado__isnull=False)
    
    return render(request, 'empleados.html', {
        'empleados': empleados,
        'usuarios_pendientes': usuarios_pendientes
    })

@login_required
@cargo_requerido("Gerente")
def ver_bitacora(request):
    bitacoras = Bitacora.objects.select_related('usuario').order_by('-fecha')
    return render(request, 'bitacora.html', {'bitacoras': bitacoras})

@login_required
@cargo_requerido("Gerente")
def asignar_empleado(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    cargos = CargoLaboral.objects.all()
    
    if request.method == "POST":
        cargo_id = request.POST.get('cargo')
        cargo = CargoLaboral.objects.get(id=cargo_id)
        # Crear registro de Empleado sin todos los datos todavía
        Empleado.objects.create(usuario=usuario, cargo=cargo, estado=False)
        # Redirigir o mostrar mensaje
        return redirect('ver_empleados')
    
    return render(request, 'asignar_empleado.html', {'usuario': usuario, 'cargos': cargos})