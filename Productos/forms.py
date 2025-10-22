from django import forms
from .models import Categoria,Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'categoria_padre']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'cantidad', 'unidad_medida', 'precio_venta', 'categoria', 'imagen']