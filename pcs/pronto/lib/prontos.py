from django.db.models import Q
from django.db import connection

from .date import *
from ..config import *
from .jsonkit import *
from ..models import Pronto
from .wrapper import *
from .filter import clean_request_filter


def update_prontos_fields(pronto_info_dic):
    for req_pronto_id in pronto_info_dic:
        pronto = Pronto.objects.get_or_create(pronto_id=req_pronto_id,
                                              group_idx=pronto_info_dic[req_pronto_id]["group_idx"])[0]
        update_pronto_fields(req_pronto_id, pronto_info_dic, pronto)


def update_pronto_fields(pronto_id, pronto_info, pronto_instance):
    for field in pronto_info[pronto_id]:
        if field in get_pronto_fields():
            setattr(pronto_instance, field, pronto_info[pronto_id][field])
            #setattr(object, name, value)
    pronto_instance.save()


def get_pronto_with_filter(filter_cleaned):
    expression_sql = 'SELECT * FROM pronto_pronto WHERE '
    has_and = False
    for field in filter_cleaned:
        if has_and:
            expression_sql += " AND " + field + " LIKE '%" + filter_cleaned[field] + "%'"
        else:
            expression_sql += field + " LIKE '%" + filter_cleaned[field] + "%'"
            has_and = True
    return Pronto.objects.raw(expression_sql)


def update_pronto_attr(pronto_instance):
    return dict([(attr, getattr(pronto_instance, attr)) for attr in get_pronto_fields()])


def get_current_week_pronto():
    return Pronto.objects.filter(Q(out_date=None) | Q(out_date__range=get_current_week_range()))


@wrapper_cache
def get_pronto_fields():
    return [f.name for f in Pronto._meta.fields if f.name != "id"]


@wrapper_cache
def get_pronto_all():
    return Pronto.objects.all()


@wrapper_cache
def get_current_week_pronto_status():
    json_list = []
    for pronto_instance in Pronto.objects.filter(Q(out_date=None) | Q(out_date__range=get_current_week_range())):
        json_list.append(
            dict([(attr, getattr(pronto_instance, attr))
                  for attr in get_pronto_fields()
                  if getattr(pronto_instance, attr)]))
    return json_list


def get_pronto_with_fitler(request_filter):
    json_list = []
    filter_cleaned = clean_request_filter(request_filter)
    if filter_cleaned:
        filtered_pronto = get_pronto_with_filter(filter_cleaned)
    else:
        filtered_pronto = get_pronto_all()
    for pronto_instance in filtered_pronto:
        json_list.append(update_pronto_attr(pronto_instance))
    return json_list


@wrapper_cache
def get_prontos_time():
    statics_result = dict()
    statics_result["pronto_id"] = []
    statics_result["time_rft"] = []
    statics_result["time_test"] = []
    prontos_closed = Pronto.objects.filter(status="Closed")
    for pronto in prontos_closed:
        statics_result["pronto_id"].append(pronto.pronto_id)
        statics_result["time_rft"].append(pronto.time_rft())
        statics_result["time_test"].append(pronto.time_test())
    return statics_result


@wrapper_cache
def get_prontos_top():
    status = "Closed"
    statics_result = dict()
    statics_result["count_top"] = []
    statics_result["count_no_top"] = []
    statics_result["date"] = []
    all_weeks_list = get_all_weeks_range()
    for date_from, date_to, week_stat in all_weeks_list:
        result = False
        count_top = Pronto.objects.filter(out_date__range=(date_from, date_to), status=status, is_top="true").count()
        count_no_top = Pronto.objects.filter(out_date__range=(date_from, date_to), status=status,
                                             is_top="false").count()
        if count_top or count_no_top:
            result = True
        if result:
            statics_result["count_top"].append(count_top)
            statics_result["count_no_top"].append(count_no_top)
            statics_result["date"].append(week_stat)
    return statics_result


@wrapper_cache_with_param
def get_prontos_ratio(attribute_receive):
    statics_result = []
    sql_raw = "SELECT " + attribute_receive + ", COUNT(id) FROM pronto_pronto GROUP BY " + attribute_receive
    if attribute_receive in STATICS_ONLY_CALCULATE_CLOSE:
        sql_raw = "SELECT " + attribute_receive + ", COUNT(id) FROM pronto_pronto WHERE status='Closed' GROUP BY " \
                  + attribute_receive
    for item in connection.cursor().execute(sql_raw).fetchall():
        if item[0]:
            statics_result.append({"name": item[0], "y": item[1]})
    return statics_result


@wrapper_cache
def get_prontos_charting():
    statics_result = {}
    for key in PRONTO_STATUS:
        statics_result[key] = []
        statics_result["date"] = []
    statics_result["Investigating"] = []
    statics_result["total"] = []
    all_weeks_list = get_all_weeks_range()
    for date_from, date_to, week_stat in all_weeks_list:
        #print(date_from,date_to,week_stat)
        #2019-04-01 00:00:00 2019-04-08 00:00:00 2019-13
        tmp_date_dic = {}
        result = False
        for stat in PRONTO_STATUS:
            #PRONTO_STATUS ['Closed', 'Transferred', 'CNN']
            count = Pronto.objects.filter(out_date__range=(date_from, date_to), status=stat).count()
            tmp_date_dic[stat] = count
            if count:
                result = True
            elif date_from.strftime('%Y-%W') == get_time_format(get_time_now()):
                result = True
        if result:
            total_counter = 0
            statics_result["date"].append(week_stat)
            for key in PRONTO_STATUS:
                total_counter += tmp_date_dic[key]
                statics_result[key].append(tmp_date_dic[key])
            investigating_count_1 = Pronto.objects.filter(in_date__lte=date_from, out_date__gt=date_to).count()
            investigating_count_2 = Pronto.objects.filter(in_date__lte=date_to, status="Ongoing").count()
            investigating_count = investigating_count_1 + investigating_count_2
            statics_result["Investigating"].append(investigating_count)
            total_counter += investigating_count
            statics_result["total"].append(total_counter)
    return statics_result
    #{'Closed': [0, 0], 'date': ['2019-12', '2019-13'], 'Transferred': [2, 5], 'CNN': [0, 1], 'Investigating': [5, 6], 'total': [7, 12]}


@wrapper_cache
def get_prontos_charting_day():
    statics_result = {}
    for key in PRONTO_STATUS:
        statics_result[key] = []
        statics_result["date"] = []
    statics_result["Investigating"] = []
    statics_result["total"] = []
    tmp_date_dic = {}
    result = False
    total_counter = 0
    for stat in PRONTO_STATUS:
        #PRONTO_STATUS ["Closed", "Inflow", "CNN", "Outflow"]
        count_inflow = Pronto.objects.filter(in_date__contains=get_time_now().strftime('%Y-%m-%d'),status=stat).count()
        count_outflow = Pronto.objects.filter(out_date__contains=get_time_now().strftime('%Y-%m-%d'), status=stat).count()
        print(get_time_now().strftime('%Y-%m-%d'))
        print(count_inflow,count_outflow)
        tmp_date_dic["Inflow"] = count_inflow
        tmp_date_dic["Outflow"] = count_outflow
        #if count_inflow:
        #    statics_result['Inflow'].append(tmp_date_dic['Inflow']
        #    total_counter += tmp_date_dic['Inflow']
        #elif count_outflow:
        #    statics_result["Outflow"].append(tmp_date_dic["Outflow"])
        #    total_counter += tmp_date_dic["Outflow"]
    statics_result["date"].append(get_time_now().strftime('%Y-%m-%d'))
    investigating_count = Pronto.objects.filter(status="Ongoing").count()
    statics_result["Investigating"].append(investigating_count)
    total_counter += investigating_count
    statics_result["total"].append(total_counter)
    #{"Closed": [0], "date": ["2019-04-05-00"], "Transferred": [7], "CNN": [1], "Investigating": [6], "total": [14]}
    return statics_result


@wrapper_cache
def get_prontos_priority():
    status = "Closed"
    statics_result = dict()
    statics_result["A - Critical"] = []
    statics_result["B - Major"] = []
    statics_result["C - Minor"] = []
    statics_result["date"] = []
    all_weeks_list = get_all_weeks_range()
    for date_from, date_to, week_stat in all_weeks_list:
        result = False
        priority_a_counter = Pronto.objects.filter(out_date__range=(date_from, date_to), status=status,
                                                   severity="A - Critical").count()
        priority_b_counter = Pronto.objects.filter(out_date__range=(date_from, date_to), status=status,
                                                   severity="B - Major").count()
        priority_c_counter = Pronto.objects.filter(out_date__range=(date_from, date_to), status=status,
                                                   severity="C - Minor").count()
        if priority_a_counter or priority_b_counter or priority_c_counter:
            result = True
        if result:
            statics_result["A - Critical"].append(priority_a_counter)
            statics_result["B - Major"].append(priority_b_counter)
            statics_result["C - Minor"].append(priority_c_counter)
            statics_result["date"].append(week_stat)
    return statics_result

def delete_prontos(pronto_id):
    Pronto.objects.get(pronto_id=pronto_id).delete()

def get_prontos_not_done(group_idx):
    return [pronto_instance.pronto_id for pronto_instance in
            Pronto.objects.filter(out_date=None, group_idx=group_idx)]


# TODO This was only used for previous datebase load
# def load_to_database(pronto_list):
#     for pronto in pronto_list:
#         pronto_instance = Pronto.objects.get_or_create(pronto_id=pronto["pronto_id"],group_idx=pronto["group_idx"])[0]
#         for filed in pronto:
#             if filed != "id":
#                 setattr(pronto_instance, filed, pronto[filed])
#         pronto_instance.save()
