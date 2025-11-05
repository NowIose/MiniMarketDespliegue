from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import openpyxl
from openpyxl.styles import Font, Alignment


def render_to_pdf(template_src, context, filename="reporte.pdf"):
    """
    Genera un PDF a partir de un template HTML y un contexto.
    """
    template = get_template(template_src)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response


def render_to_excel(headers, rows, filename="reporte.xlsx", gran_total=None):
    """
    Genera un Excel a partir de encabezados y filas de datos.
    - headers: lista de nombres de columnas
    - rows: lista de listas con los valores de cada fila
    - gran_total: valor opcional para mostrar al final
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte"

    # Encabezados
    ws.append(headers)
    for col in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Filas de datos
    for row in rows:
        ws.append(row)

    # Gran total opcional
    if gran_total is not None:
        ws.append([""] * (len(headers) - 2) + ["Gran Total", gran_total])

    # Respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response