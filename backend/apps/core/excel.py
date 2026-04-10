from io import BytesIO
from django.http import HttpResponse
from openpyxl import Workbook

def export_as_excel(filename, headers, queryset, row_builder, sheet_name="Data"):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.append(headers)
    for obj in queryset:
        ws.append(row_builder(obj))
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
