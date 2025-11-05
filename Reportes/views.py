"""Views para la app de Reportes"""
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render
from Reportes.utils.reportes import render_to_excel, render_to_pdf
from Usuarios.models import Cliente
from Ventas.models import Venta

# Create your views here.
from django.shortcuts import render


@login_required
def panel_reportes(request):
    """Vista para el panel general de reportes"""

    clientes = getattr(Cliente, 'objects').values(
        "usuario__id",
        "usuario__first_name",
        "usuario__last_name"
    )

    return render(request, 'reportes/panel.html', {
        'clientes' : clientes,
    })

def reporte_ventas(request):
    """
    Genera el reporte de ventas segun los fitros aplicados y los exporta en
    el formato escogido Pdf o Excel
    """

    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")
    cliente = request.GET.get("cliente")
    formato = request.GET.get("formato")    # Pdf o Excel

    # Iniciar el queryset base
    ventas = getattr(Venta, 'objects').all()

    # Aplicar filtros condicionalmente
    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            ventas = ventas.filter(fecha__gte=fecha_inicio)
        except ValueError:
            pass

    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            ventas = ventas.filter(fecha__lte=fecha_fin)
        except ValueError:
            pass

    if cliente and cliente != "todos":
        ventas = ventas.filter(cliente_id=cliente)

    for venta in ventas:
        venta.total = venta.total_venta # total_venta es una propiedad del modelo Venta

    # Gran total acumulado
    gran_total = sum(v.total for v in ventas)

    context = {
        'ventas': ventas, 
        'fecha_inicio': fecha_inicio, 
        'fecha_fin': fecha_fin,
        'cliente': cliente,
        'gran_total': gran_total
    }

    if formato == "pdf":
        return render_to_pdf("reportes/reporte_ventas_pdf.html", context, "reporte_ventas.pdf")

    elif formato == "excel":
        headers = ["Fecha", "Cliente", "Empleado", "Pago", "Total"]
        #rows = [[v.fecha, v.id_cliente, v.empleado, v.pago, v.total] for v in ventas]
        rows = [
        [
        v.fecha,
        v.id_cliente.usuario.username,
        v.id_empleado.usuario.username,
        v.id_pago.descripcion,
        float(v.total),
        ]
    for v in ventas
]
        return render_to_excel(headers, rows, "reporte_ventas.xlsx", gran_total)