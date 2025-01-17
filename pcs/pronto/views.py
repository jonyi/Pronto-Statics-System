from django.shortcuts import render
from django.views.decorators.cache import cache_page

from .lib.http import *
from .lib.mail import *
from .lib.cache import *
from .lib.prontos import *


@cache_page(CACHE_TIME)
def index(request):
    return render(request, 'pronto/index.html', {"pronto_fields": get_pronto_fields()})

def update_pronto(request):
    idx = int(request.POST.get('content[id]'))
    pronto_instance = Pronto.objects.get(id=idx)
    for field in request.POST:
        if "content" in field:
            setattr(pronto_instance, field.split("[")[-1][:-1], request.POST.get(field))
    pronto_instance.save()
    return HttpResponse(pronto_instance.to_json(), content_type="application/json")


def create_or_update_pronto(request):
    clear_cache()
    pronto_info_dic = get_dic_from_json(request.body)
    update_prontos_fields(pronto_info_dic)
    return http_reponse()


@cache_page(CACHE_TIME)
def render_pronto_statics(request):
    return render(request, 'pronto/static.html')


@cache_page(CACHE_TIME)
def render_pronto_charting(request):
    return render(request, 'pronto/charting.html', {"pronto_fields": get_pronto_fields()})


def get_pronto_woh(request):
    return http_response_with_json(get_current_week_pronto_status())


def get_pronto_all(request):
    req_filter = request.GET
    return http_response_with_json(get_pronto_with_fitler(req_filter))


def get_pronto_top(request):
    return http_response_with_json(get_prontos_top())


def get_pronto_time(request):
    return http_response_with_json(get_prontos_time())


def get_pronto_ratio(request):
    attribute = request.GET["attribute"]
    return http_response_with_json(get_prontos_ratio(attribute))


def get_pronto_report(request):
    send_prontos_report()
    return http_reponse("<h1>Mail Sent Successfully!</h1>")


def get_pronto_charting(request):
    return http_response_with_json(get_prontos_charting())

def get_pronto_charting_day(request):
    return http_response_with_json(get_prontos_charting_day())

def get_pronto_priority(request):
    return http_response_with_json(get_prontos_priority())

def delete_pronto(request):
    pronto_id = request.GET.get("pronto_id")
    return  http_response_with_json(delete_prontos(pronto_id))


def get_pronto_not_done(request):
    group = request.GET.get("group")
    return http_response_with_json(get_prontos_not_done(group))




















