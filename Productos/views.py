from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Producto

@login_required
def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})