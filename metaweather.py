import requests

day_of_week = {
    0: 'Ponedjeljak',
    1: 'Utorak',
    2: 'Srijeda',
    3: 'Četvrtak',
    4: 'Petak',
    5: 'Subota',
    6: 'Nedjelja'
}

weather_state_abr = {
    'sn': 'Snijeg',
    'sl': 'Susnježica',
    'h': 'Tuča',
    't': 'Grmljavina',
    'hr': 'Pljusak',
    'lr': 'Slaba kiša',
    's': 'Kratki pljuskovi',
    'lc': 'Blaga naoblaka',
    'hc': 'Oblačno',
    'c': 'Vedro'
}

city_woeid = '851128'  # Zagreb woeid
api_woeid_url = 'https://www.metaweather.com/api/location/'
api_zagreb_url = 'https://www.metaweather.com/api/location/851128'


def get_api_icon(icon_abr):
    return 'https://www.metaweather.com/static/img/weather/png/' + icon_abr + '.png'


def get_forecast():
    jsonurl = requests.get(api_zagreb_url)  # todo returna string (slack block)
    return jsonurl


def get_today_forecast():  # todo returna posloženi blok za
    return 1

