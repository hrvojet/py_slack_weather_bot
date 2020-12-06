import requests
import re

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
    'hr': 'Kiša',
    'lr': 'Lagana kiša',
    's': 'Kratki pljuskovi',
    'lc': 'Blaga naoblaka',
    'hc': 'Oblačno',
    'c': 'Vedro'
}

city_woeid = '851128'  # Zagreb woeid
api_woeid_url = 'https://www.metaweather.com/api/location/'
api_zagreb_url = 'https://www.metaweather.com/api/location/851128'


def get_forecast():
    jsonurl = requests.get(api_zagreb_url)
    return jsonurl


def not_valid_text(text):
    digits = re.findall(r'\d+', text)
    digits = list(map(int, digits))
    if len(digits) != 1 or not(0 <= digits[0] <= 23):
        return True
    return False
