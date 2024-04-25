import requests
import json
from concurrent.futures import ThreadPoolExecutor
from celery import Celery
import time
import datetime


celery = Celery('tasks', broker='redis://redis:6379/0')


def gen_json(headers, id):
    """Получение данных из аккаунта и генерация json для принятия заявки"""
    request_url = f'https://dobro.ru/api/v2/volunteers/{id}?id={id}&with=organizer%2Cdj_articles_count%2Cvolunteer_reviews_count%2Curl%2Ccan_contact%2Ctrophy%2Cedit_info%2CeduCertificates%2Ccourse%2Cevent%2CeditableTags%2Cesia%2Ccourses_count%2Cbookmark'
    while True:
        try:
            r = json.loads(requests.get(request_url, headers=headers).text)
            break
        except:
            continue
        
    template_json = {
    "fields": {
        "request_field_42": {
            "last_name": r.get('fio', {}).get('last_name', ''),
            "first_name": r.get('fio', {}).get('first_name', ''),
            "second_name": r.get('fio', {}).get('second_name', '')
        },
        "request_field_43": r.get('birthday', '')[:10] + "T10:00:00.000Z",
        "request_field_46": {
            "value": r.get('settlement', {}).get('title', ''),
            "data": {
                "region_kladr_id": r.get('settlement', {}).get('region', ''),
                "settlement": r.get('settlement', {}).get('settlement', ''),
                "settlement_kladr_id": r.get('settlement', {}).get('settlementCode', ''),
                "geo_lat": r.get('settlement', {}).get('y', ''),
                "geo_lon": r.get('settlement', {}).get('x', '')
            }
        },
        "request_field_18650": r.get('volunteerOrganization', {}).get('name', ''),
        "request_field_211697": {"label": "Россия", "value": "Россия"},
        "request_field_49": {"value": r.get('gender', ''), "label": r.get('gender', '')},
        "request_field_52": "очень хочу помочь",
        "request_field_48": {"label": r.get('translatedGender', ''), "value": r.get('translatedGender', '')},
        "request_field_47": r.get('telephone', ''),
        "request_field_email": r.get('user', {}).get('email', ''),
        "request_field_18652": r.get('socialMedia', {}).get('vk', ''),
        "request_field_150870": r.get('socialMedia', {}).get('telegram', ''),
        "request_field_18503": {
            "value": r.get('passport', {}).get('address', {}).get('title', ''),
            "data": {"region_kladr_id": r.get('settlement', {}).get('region', ''), "settlement": r.get('settlement', {}).get('settlement', ''), "settlement_kladr_id": r.get('settlement', {}).get('settlementCode', ''), "house": r.get('actualAddress', {}).get('house', ''), "geo_lat": r.get('settlement', {}).get('y', ''), "geo_lon": r.get('settlement', {}).get('x', '')}
        },
        "request_field_53": {"value": r.get('educationLevel', {}).get('id', ''), "label": r.get('educationLevel', {}).get('title', '')},
        "request_field_54": [{"institutionName": bg.get('institutionName', ''), "speciality": bg.get('speciality', ''), "fromYear": {"value": bg.get('fromYear', {}).get('value', '') if isinstance(bg.get('fromYear', {}), dict) else '', "label": bg.get('fromYear', {}).get('label', '') if isinstance(bg.get('fromYear', {}), dict) else ''}, "toYear": {"value": bg.get('toYear', {}).get('value', '') if isinstance(bg.get('toYear', {}), dict) else '', "label": bg.get('toYear', {}).get('label', '') if isinstance(bg.get('toYear', {}), dict) else ''}} for bg in r.get('educationBackgrounds', [{'institutionName': '', 'speciality': '', 'fromYear': {'value': '', 'label': ''}, 'toYear': {'value': '', 'label': ''}}])],
        "request_field_18648": {"value": r.get('employmentType', {}).get('id', ''), "label": r.get('employmentType', {}).get('title', '')},
        "request_field_18651": [{"organizationName": job.get('organizationName', ''), "position": job.get('position', '')} for job in r.get('jobs', [{'organizationName': '', 'position': ''}])]
    },
    "terms_of_use": True,
    "requirements": [],
    "periods": []
    }
    return template_json


def get_token(email, password):
    url = 'https://dobro.ru/token'
    payload = {
    'grant_type': 'password',
    'client_id': '5b2a8caa9d6176bf92b331ff14bca068',
    'client_secret': 'eca9812eed02421ebaf05e7e0e5a53607e9cb36f8f26b14251a370bf6b8929b97575424bdb9b010e4f294d47120aa0c039107c6f332636c772240c885f32a47f',
    'username': email,
    'password': password
    }
    try:
        response = requests.post(url, data=payload)
        return json.loads(response.text)['access_token']
    except:
        return 'error'



def parse_event_ids():
    date = datetime.date.today()
    event_ids = []
    for i in range(1, 16):
        url = f'https://dobro.ru/api/v2/frontend/events/search?t=e&d_c=1&d_s=1&%3Futm_source=dobroru&utm_medium=organic&utm_campaign=promo&utm_content=headerservices&e%5Bsettlement%5D%5Btitle%5D=&e%5BfromDate%5D={datetime.datetime.now().strftime("%d.%m.%Y")}&e%5BtoDate%5D=09.04.2027&e%5BorderBy%5D%5BpublicationDate%5D=desc&e%5Bonline%5D=1&e%5Bquery%5D=&e%5BnotAdultOnly%5D=1&vl%5Bsettlement%5D%5Btitle%5D=&o%5Bsettlement%5D%5Btitle%5D=&p%5Bsettlement%5D%5Btitle%5D=&all%5Bsettlement%5D%5Btitle%5D=&page={i}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            event_ids.extend(data.get('ids', []))
    print(len(event_ids))
    return event_ids

def delete_fields(id, jso, headers):
    url = f'https://dobro.ru/api/v2/vacancy/{id}/request'
    r = requests.get(url, headers=headers).text
    fields = [i['id'] for i in json.loads(r)['fields']]
    new_json = filter_fields(jso, fields)
    return new_json
    
def filter_fields(data, fields):
    if not isinstance(data, dict):
        return data
    for key in list(data.keys()):
        if key == 'fields':
            subfields = data[key]
            for subfield_key in list(subfields.keys()):
                if subfield_key not in fields:
                    del subfields[subfield_key]
        else:
            data[key] = filter_fields(data[key], fields)
    return data    

def add_request(event_id, template_json, headers):
    url = f'https://dobro.ru/event/{event_id}'
    page = requests.get(url).text
    try:
        if 'create_disabled' not in page:
            event_vacancy_start = page.index('"eventVacancies":[{"id"')
            vacancy_id = page[event_vacancy_start + 24:event_vacancy_start + 32]
            request_url = f'https://dobro.ru/api/v2/vacancy/{vacancy_id}/request'
            input_json = json.loads(requests.get(request_url, headers=headers).text)
            output_json = convert_json(input_json, template_json)
            output_json = delete_fields(vacancy_id, output_json, headers)
            data = json.loads(json.dumps(output_json, ensure_ascii=False, indent=4))
            response = requests.post(request_url, headers=headers, json=data)
            return [response.status_code, event_id]
    except ValueError:
        ...

def convert_json(input_json, template_json):
    output_json = template_json
    for period in input_json["timeSettings"]:
        output_json["periods"].append({
            "from_date": '.'.join(period["date"].split('.')[::-1]).replace('.', '-'),
            "key": period["date"],
            "to_date": '.'.join(period["date"].split('.')[::-1]).replace('.', '-')
        })
    return output_json


@celery.task
def parser(headers, template_json):
    event_ids = parse_event_ids()
    responses = []
    def add_request_and_collect_results(event_id, template_json, headers):
        response = add_request(event_id, template_json, headers)
        if response[0] == 201:
            responses.append(response[0])

    with ThreadPoolExecutor() as executor:
        executor.map(add_request_and_collect_results, event_ids, [template_json]*len(event_ids), [headers]*len(event_ids))

    return len(responses)

