from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


# '''@login_required
# def ver_productos(request):
#     productos = Producto.objects.all()
#     return render(request, 'productos.html', {'productos': productos})'''
#@login_required
# def ver_productos(request):
#     empleado = getattr(request.user, 'empleado', None)
#     # Permitir si es empleado y ya completó (estado=True)
#     if not empleado or not empleado.estado:
#         messages.warning(request, "Debes completar tu registro de empleado para acceder a productos.")
#         # Si tiene asignación pero incompleta, mandarlo a completar
#         if empleado:
#             return redirect('completar_empleado')
#         return redirect('home')

#     productos = Producto.objects.all()
#     return render(request, 'productos.html', {'productos': productos})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Función para verificar si el usuario es gerente
def es_gerente(user):
    return user.groups.filter(name='Gerente').exists()
# 🔹 Ver categorías principales
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.filter(categoria_padre__isnull=True)
    return render(request, 'producto/listar_categorias.html', {
        'categorias': categorias,
        'es_gerente': es_gerente(request.user)
    })
# 🔹 Ver detalle de una categoría: subcategorías y productos
@login_required
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    subcategorias = Categoria.objects.filter(categoria_padre=categoria)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'producto/productos_por_categoria.html', {
        'categoria': categoria,
        'subcategorias': subcategorias,
        'productos': productos,
        'es_gerente': es_gerente(request.user)
    })



# Función para verificar si el usuario es gerente

@login_required
@user_passes_test(es_gerente, login_url='listar_categorias')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'producto/crear_categoria.html', {'form': form})

@login_required
def ver_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    subcategorias = categoria.subcategorias.all()
    productos = Producto.objects.filter(categoria=categoria)

    return render(request, 'producto/ver_categoria.html', {
        'categoria': categoria,
        'subcategorias': subcategorias,
        'productos': productos,
        'es_gerente': es_gerente(request.user)
    })


# 🔹 Crear subcategoría (solo Gerente)
@login_required
@user_passes_test(es_gerente, login_url='listar_categorias')
def crear_subcategoria(request, categoria_id):
    categoria_padre = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            Categoria.objects.create(nombre=nombre, categoria_padre=categoria_padre)
            messages.success(request, f"Subcategoría '{nombre}' agregada correctamente.")
            return redirect('ver_categoria', categoria_id=categoria_padre.id)

    return render(request, 'producto/crear_subcategoria.html', {'categoria_padre': categoria_padre})


# 🔹 Crear producto (solo Gerente)
@login_required
@user_passes_test(es_gerente, login_url='listar_categorias')
def crear_producto(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        unidad_medida = request.POST.get('unidad_medida')
        precio_venta = request.POST.get('precio_venta')

        if nombre and precio_venta:
            Producto.objects.create(
                nombre=nombre,
                cantidad=cantidad or 0,
                unidad_medida=unidad_medida or "Unidad",
                precio_venta=precio_venta,
                categoria=categoria
            )
            messages.success(request, f"Producto '{nombre}' agregado correctamente.")
            return redirect('ver_categoria', categoria_id=categoria.id)

    return render(request, 'producto/crear_producto.html', {'categoria': categoria})