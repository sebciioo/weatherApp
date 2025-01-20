import requests
from flask import current_app


"""
    Zawiera funkcje do pobierania danych pogodowych z różnych API, w tym aktualne dane pogodowe, prognozy i jakość powietrza.
"""


def fetch_weather_data(lat, lon):
    api_key = current_app.config['WEATHER_API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_air_quality_data(lat, lon):
    api_key = current_app.config['WEATHER_API_KEY']
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_current_weather_data(lat, lon):
    api_key = current_app.config['WEATHER_API_KEY']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None