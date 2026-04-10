import csv
from django.http import HttpResponse

def export_as_csv(filename, field_names, queryset, row_builder):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow(row_builder(obj))
    return response
