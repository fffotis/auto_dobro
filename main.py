from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
from task import *



app = FastAPI()

print(1)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def index(request: Request):
    form = """
    <!DOCTYPE html>
    <html lang="ru">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AUTO DOBRO</title>
        <link rel="styleshtaskt" href="static/styles.css"> </head>

        <body>
        <div class="instruction">
            <form class="instruction-form" method="post">
            <label for="input_text">Введите email:</label>
            <input type="text" id="input_text" name="input_text">
            <label for="password">Введите пароль:</label>
            <input type="text" id="password" name="password">
            <button type="submit">Отправить</button>
            </form>
            </div>
        </body>
    </html> 
    """
    return HTMLResponse(form)

def f(headers, id):
    request_url = f'https://dobro.ru/api/v2/volunteers/{id}?id={id}&with=organizer%2Cdj_articles_count%2Cvolunteer_reviews_count%2Curl%2Ccan_contact%2Ctrophy%2Cedit_info%2CeduCertificates%2Ccourse%2Cevent%2CeditableTags%2Cesia%2Ccourses_count%2Cbookmark'
    while True:
        try:
            r = json.loads(requests.get(request_url, headers=headers).text)
            break
        except:
            continue
        
    try:
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
    except:
        return 'data error'

@app.post("/", response_class=HTMLResponse)
def post_form(request: Request, input_text: str = Form(...), password: str = Form(...)):
    email = input_text
    password = password
    token = get_token(email, password)
    if token == 'error':
        return 'error'
    headers = {
        'Authorization': f'Bearer {token}' ,
        'Content-Type': 'application/json'
    }
    id = json.loads(requests.get('https://dobro.ru/api/v2/auth/me?groups[]=id:read', headers=headers).text)['id']
    template_json = f(headers, id)
    print(template_json)
    if template_json == 'data error':
        return 'заполни профиль'
    parser.delay(headers, template_json)    
    return f"Чётко. Можешь закрыть страницу."

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')