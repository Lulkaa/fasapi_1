import requests
from datetime import datetime, timedelta
from fastapi import FastAPI
from dateutil.parser import parse

app = FastAPI()


@app.get('/info/',tags = ["Info"])
def info():
    return {
        'author': 'Yulia Chepak',
        '/info': "Інформація про додаток",
        '/get/all/': 'Виводить CVE за останні 5 днів(Змінила на 10,бо за 5 нічого немає). Максимум 40 CVE.',
        '/get/new/': 'Виводить 10 найновіших CVE',
        '/get/known': 'Виводить CVE в яких knownRansomwareCampaignUse - Known, максимум 10',
        '/get': 'Виводить CVE яке містить ключове слово,',

    }
@app.get('/get/all/',tags = ["Last 5 days CVE"])
def all():
    response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    days = datetime.now() - timedelta(days=10) # Змінила тут на 10, бо на 5 немає даних
    list = []
    for item in response.json()['vulnerabilities']:
        if "dateAdded" in item and parse(item["dateAdded"]).date() >= days.date():
            list.append(item)
    return {'vulnerabilities': list[:40]}


@app.get('/get/new/',tags = ["Last 10 CVE"])
def new():
    response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    return response.json()['vulnerabilities'][:10] # так як файл посортований, просто поверну 10 перших значень


@app.get('/get/known',tags = ["Key value = known"])
def known():
    response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    list = []
    for item in response.json()['vulnerabilities']:
        if item['knownRansomwareCampaignUse'] == 'Known':
            list.append(item)
    return list[:10]


@app.get('/get/',tags = ["Enter key word "])
def keyword(query: str):
    response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    list = []
    for item in response.json()['vulnerabilities']:
        if any(query.lower() in str(value).lower() for value in item.values()):
            list.append(item)
    return {'vulnerabilities': list}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)