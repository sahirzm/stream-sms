from django.db.models.fields import DateField, DateTimeField
from django.http.response import JsonResponse


def dateToStr(date, strip_time=False):

    if date is None or not (isinstance(date, DateField) or isinstance(date, DateTimeField)):
        return ""
    else:
        if isinstance(date, DateField) or strip_time:
            return date.strftime("%m-%d-%Y")
        elif isinstance(date, DateTimeField):
            return date.strftime("%m-%d-%Y %H:%M:%S")

def handle_validation_error(ve):
    response = JsonResponse(ve.message_dict)
    response.status_code = 422
    return response

def add_validation_error(errors, field, message):
    errors.setdefault(field, []).append(message)

