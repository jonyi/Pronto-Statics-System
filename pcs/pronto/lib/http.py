import json

from django.http import HttpResponse

from .dateencoder import DateEncoder


def http_response_with_json(statics_result):
    return HttpResponse(json.dumps(statics_result, cls=DateEncoder), content_type="application/json")


def http_reponse(content=None):
    if content:
        return HttpResponse(content)
    else:
        return HttpResponse()
