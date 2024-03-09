import requests
import json
from concurrent.futures import ThreadPoolExecutor
from celery import Celery




celery = Celery('tasks', broker='redis://redis:6379/0')

@celery.task
def parser(token, headers, template_json ):
    def parse_event_ids():
        event_ids = []
        for i in range(1, 10):
            url = f'https://dobro.ru/api/v2/frontend/events/search?t=e&d_c=1&d_s=1&%3Futm_source=dobroru&utm_medium=organic&utm_campaign=promo&utm_content=headerservices&e%5Bsettlement%5D%5Btitle%5D=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C+%D0%9D%D0%B0%D0%B7%D1%80%D0%B0%D0%BD%D1%8C&e%5Bsettlement%5D%5Bregion%5D=6&e%5Bsettlement%5D%5Bmunicipality%5D=&e%5Bsettlement%5D%5BmunicipalityCode%5D=&e%5Bsettlement%5D%5Bhouse%5D=&e%5Bsettlement%5D%5Bflat%5D=&e%5Bsettlement%5D%5Blat%5D=43.225727&e%5Bsettlement%5D%5Blon%5D=44.764641&e%5Bsettlement%5D%5BcountryCode%5D=&e%5Bsettlement%5D%5Bsettlement%5D=&e%5Bsettlement%5D%5BsettlementCode%5D=&e%5Bsettlement%5D%5Bstreet%5D=&e%5BfromDate%5D=09.03.2024&e%5BtoDate%5D=09.03.2027&e%5Bonline%5D=1&e%5Bverified%5D=1&e%5BnotAdultOnly%5D=1&e%5Bparticipant%5D=1&e%5Btags%5D%5B0%5D=83763&vl%5Bsettlement%5D%5Btitle%5D=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C+%D0%9D%D0%B0%D0%B7%D1%80%D0%B0%D0%BD%D1%8C&vl%5Bsettlement%5D%5Bregion%5D=6&vl%5Bsettlement%5D%5Bmunicipality%5D=&vl%5Bsettlement%5D%5BmunicipalityCode%5D=&vl%5Bsettlement%5D%5Bhouse%5D=&vl%5Bsettlement%5D%5Bflat%5D=&vl%5Bsettlement%5D%5Blat%5D=43.225727&vl%5Bsettlement%5D%5Blon%5D=44.764641&vl%5Bsettlement%5D%5BcountryCode%5D=&vl%5Bsettlement%5D%5Bsettlement%5D=&vl%5Bsettlement%5D%5BsettlementCode%5D=&vl%5Bsettlement%5D%5Bstreet%5D=&o%5Bsettlement%5D%5Btitle%5D=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C+%D0%9D%D0%B0%D0%B7%D1%80%D0%B0%D0%BD%D1%8C&o%5Bsettlement%5D%5Bregion%5D=6&o%5Bsettlement%5D%5Bmunicipality%5D=&o%5Bsettlement%5D%5BmunicipalityCode%5D=&o%5Bsettlement%5D%5Bhouse%5D=&o%5Bsettlement%5D%5Bflat%5D=&o%5Bsettlement%5D%5Blat%5D=43.225727&o%5Bsettlement%5D%5Blon%5D=44.764641&o%5Bsettlement%5D%5BcountryCode%5D=&o%5Bsettlement%5D%5Bsettlement%5D=&o%5Bsettlement%5D%5BsettlementCode%5D=&o%5Bsettlement%5D%5Bstreet%5D=&p%5Bsettlement%5D%5Btitle%5D=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C+%D0%9D%D0%B0%D0%B7%D1%80%D0%B0%D0%BD%D1%8C&p%5Bsettlement%5D%5Bregion%5D=6&p%5Bsettlement%5D%5Bmunicipality%5D=&p%5Bsettlement%5D%5BmunicipalityCode%5D=&p%5Bsettlement%5D%5Bhouse%5D=&p%5Bsettlement%5D%5Bflat%5D=&p%5Bsettlement%5D%5Blat%5D=43.225727&p%5Bsettlement%5D%5Blon%5D=44.764641&p%5Bsettlement%5D%5BcountryCode%5D=&p%5Bsettlement%5D%5Bsettlement%5D=&p%5Bsettlement%5D%5BsettlementCode%5D=&p%5Bsettlement%5D%5Bstreet%5D=&all%5Bsettlement%5D%5Btitle%5D=%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%2C+%D0%9D%D0%B0%D0%B7%D1%80%D0%B0%D0%BD%D1%8C&all%5Bsettlement%5D%5Bregion%5D=6&all%5Bsettlement%5D%5Bmunicipality%5D=&all%5Bsettlement%5D%5BmunicipalityCode%5D=&all%5Bsettlement%5D%5Bhouse%5D=&all%5Bsettlement%5D%5Bflat%5D=&all%5Bsettlement%5D%5Blat%5D=43.225727&all%5Bsettlement%5D%5Blon%5D=44.764641&all%5Bsettlement%5D%5BcountryCode%5D=&all%5Bsettlement%5D%5Bsettlement%5D=&all%5Bsettlement%5D%5BsettlementCode%5D=&all%5Bsettlement%5D%5Bstreet%5D=&page{i}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                event_ids.extend(data.get('ids', []))
        return event_ids

    def add_request(event_id):
        url = f'https://dobro.ru/event/{event_id}'
        page = requests.get(url).text
        try:
            if 'create_disabled' not in page:
                event_vacancy_start = page.index('"eventVacancies":[{"id"')
                vacancy_id = page[event_vacancy_start + 24:event_vacancy_start + 32]
                request_url = f'https://dobro.ru/api/v2/vacancy/{vacancy_id}/request'
                input_json = json.loads(requests.get(request_url, headers=headers).text)
                output_json = convert_json(input_json)
                data = json.loads(json.dumps(output_json, ensure_ascii=False, indent=4))
                response = requests.post(request_url, headers=headers, json=data)
        except ValueError:
            ...


    def convert_json(input_json):
        output_json = template_json
        
        for period in input_json["timeSettings"]:
            output_json["periods"].append({
                "from_date": '.'.join(period["date"].split('.')[::-1]).replace('.', '-'),
                "key": period["date"],
                "to_date": '.'.join(period["date"].split('.')[::-1]).replace('.', '-')
            })
        
        return output_json

    event_ids = parse_event_ids()
    # Добавление заявок на вакансии с использованием многопоточности
    with ThreadPoolExecutor() as executor:
        executor.map(add_request, event_ids)
    print('succeeded')