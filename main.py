from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import requests
from ee import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def index(request: Request):
    form = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AUTO DOBRO</title>
  <link rel="stylesheet" href="/static/styles.css">
</head>
<body>


  <div class="instruction">

  <form class="instruction-form" method="post">
      <label for="input_text">Введите данные:</label>
      <input type="text" id="input_text" name="input_text">
      <button type="submit">Отправить</button>
    </form>
    <h1>О сайте</h1>
    <p class="instruction-text">Если вы занимаетесь волонтерством к примеру для дополнительных баллов при поступлении, то есть такая тема что ты можешь подавать заявки на много добрых и даже ничего не делая вам могут накинуть како-то количество часов. Так вот этот сайт автоматически подписывает вас на всевозможные мероприятия и в итоге ничего не делая вы полуаете выгоду. На скрине результат за месяц.
    <img src="/static/3.png" alt="Скриншот" class="instruction-screenshot">
    <h1>инструкция</h1>
    <p class="instruction-text">1. Перейти на страницу редактирования профиля и заполнить всё что возможно. Зачастую можно вписать всё что угодно, но это на ваше усмотрение. <a href="https://dobro.ru/volunteers/edit" target="_blank">ссылка</a></p>
    <img src="/static/1.png" alt="Скриншот" class="instruction-screenshot">
    <p class="instruction-text">2. Теперь вам надо узнать ваш Bearer token. Для этого переходим в инструменты разработчика(CTRL + SHIFT + i), открываем мониторинг сети("Сеть" или "Network"), выбераем фильтр Fetch/XHR, и перезагружаем страницу. Жмем на перввый get-запрсо(смотри скрин), пролистываем вниз до поля с названием Authorization и копмруем его значение, т.е. всё что идет после Bearer. Именно это нам и надо ввести в поле выше.</p>
    <img src="/static/2.png" alt="Скриншот" class="instruction-screenshot">
    <p class="instruction-text">Если у вас ошибка token error, то вы неправельно ввели токен. Убедитесь что вы скопировали то что надо и целиком.</p>
    <p class="instruction-text">Если у вас ошибка data error, то вы не заполнили обязательные для успешного результата поля в настройках вашего аккаунта.</p>
  </div>
</body>
</html>
    """
    return HTMLResponse(form)

def f(headers):
    request_url = 'https://dobro.ru/api/v2/volunteers/96002534?id=96002534&with=organizer%2Cdj_articles_count%2Cvolunteer_reviews_count%2Curl%2Ccan_contact%2Ctrophy%2Cedit_info%2CeduCertificates%2Ccourse%2Cevent%2CeditableTags%2Cesia%2Ccourses_count%2Cbookmark'
    try:
        r = json.loads(requests.get(request_url, headers=headers).text)
        try:
            template_json = {
            "fields": {
                "request_field_42": {
                    "last_name": r['fio']['last_name'],
                    "first_name": r['fio']['first_name'],
                    "second_name": r['fio']['second_name']
                },
                "request_field_43": r['birthday'][:10] + "T10:00:00.000Z",
                "request_field_46": {
                    "value": r['settlement']['title'],
                    "data": {
                        "region_kladr_id": r['settlement']['region'],
                        "settlement": r['settlement']['settlement'],
                        "settlement_kladr_id": r['settlement']['settlementCode'],
                        "geo_lat": r['settlement']['y'],
                        "geo_lon": r['settlement']['x']
                    }
                },
                "request_field_18650":r['volunteerOrganization']['name'],
                "request_field_211697":{"label":"Россия","value":"Россия"},
                "request_field_49": {"value": r['gender'], "label": r['gender']},
                "request_field_52": "очень хочу помочь",
                "request_field_48": {"label": r['translatedGender'], "value": r['translatedGender']},
                "request_field_47": r['telephone'],
                "request_field_email": r['user']['email'],
                "request_field_18652": r['socialMedia']['vk'],
                "request_field_150870": r['socialMedia']['telegram'],
                "request_field_18503": {
                    "value": r['passport']['address']['title'],
                    "data": {"region_kladr_id":  r['settlement']['region'], "settlement": r['settlement']['settlement'], "settlement_kladr_id": r['settlement']['settlementCode'] , "house": r['actualAddress']['house'], "geo_lat": r['settlement']['y'], "geo_lon":r['settlement']['x']}
                },
                "request_field_53": {"value": r['educationLevel']['id'], "label": r['educationLevel']['title']},
                "request_field_54": [{"institutionName": r['educationBackgrounds'][0]['institutionName'], "speciality": r['educationBackgrounds'][0]['speciality'], "fromYear": {"value": 2012, "label": 2012}, "toYear": {"value": 2024, "label": 2024}}],
                "request_field_18648": {"value": r['employmentType']['id'], "label": r['employmentType']['title']},
                "request_field_18651": [{"organizationName": r['jobs'][0]['organizationName'], "position": r['jobs'][0]['position']}]
            },
            "terms_of_use": True,
            "requirements": [],
            "periods": []
        }
            return template_json
        except:
            return 'data error'
    except:
        print('token error')
        return 'token error'

@app.post("/", response_class=HTMLResponse)
def post_form(request: Request, input_text: str = Form(...)):
    token = input_text
    headers = {
            'Authorization': f'Bearer {token}' ,
            'Content-Type': 'application/json'
            }
    template_json = f(headers)
    if template_json == 'token error':
        return 'token error'
    elif template_json == 'data error':
        return 'data error'
    parser.delay(token, headers, template_json)    
    return f"Заебись. Ты в очереди. Можешь идти нахуй"

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')