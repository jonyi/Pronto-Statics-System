import os
import json

from .dateencoder import DateEncoder


def get_dic_from_json(json_data):
    return json.loads(json_data)


def json_dump(json_list):
    return json.dumps(json_list, cls=DateEncoder)


def write_json_file(json_dic, directory):
    with open(os.path.join(directory), "w") as json_file:
        json_file.write(json.dumps(json_dic, cls=DateEncoder))


def get_dic_from_json_data(json_data):
    json_dic = {'title': {
        'text': ''
    },
    'xAxis': {
        'title': "Date",
        'categories': json_data['date'],
        'type': 'category'
    },
    'yAxis': {
        'title': {
            'text': 'Number of Pronto'
        },
        'min': 0
    },
    'legend': {
        'align': 'center',
    },
    'series': [{
        'name': 'Num Of WOH',
        'data': json_data['total']
    },
        {
            'name': 'Num Of Closed',
            'data': json_data['Closed']
        },
        {
            'name': 'Num Of Transferred',
            'data': json_data['Transferred']
        },
        {
            'name': 'Num Of CNN',
            'data': json_data['CNN']
        },
        {
            'name': 'Num Of Investigating',
            'data': json_data['Investigating']
        }]
    }
    return json_dic
