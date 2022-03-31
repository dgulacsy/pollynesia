import csv
from datetime import datetime as dt
from django.http import HttpResponse
from django.core import serializers


def download(queryset, format):

    def download_csv(queryset):
        model = queryset.model
        field_names = [field.name for field in model._meta.get_fields()]
        response = HttpResponse(content_type='text/csv')
        writer = csv.writer(response)
        writer.writerow(field_names)
        for object in queryset:
            writer.writerow([getattr(object, name) for name in field_names])
        response['Content-Disposition'] = 'attachment;filename=votes_{0:%Y-%m-%d_%H-%M}.csv'.format(
            dt.now())
        return response

    def download_json(queryset):
        json_file = serializers.serialize('json', queryset)
        response = HttpResponse(json_file, content_type='text/json')
        response['Content-Disposition'] = 'attachment;filename=votes_{0:%Y-%m-%d_%H-%M}.json'.format(
        dt.now())
        return response

    download_formats = {
        'csv': download_csv,
        'json': download_json,
    }

    return download_formats[format](queryset)
