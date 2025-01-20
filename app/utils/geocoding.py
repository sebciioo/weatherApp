import requests
from flask import current_app
from app.models.country import Country

"""
    Zawiera funkcje do uzyskiwania współrzędnych geograficznych (szerokości i długości geograficznej) na 
    podstawie nazwy miasta i kraju.
"""


def get_coordinates(city_name, country_name):
    country = Country.query.filter(Country.full_name.ilike(country_name)).first()
    if not country:
        return None, None

    country_code = country.short_name
    api_key = current_app.config['WEATHER_API_KEY']
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&limit=1&appid={api_key}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None
