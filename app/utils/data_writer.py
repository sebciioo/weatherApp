from datetime import datetime
from app.models.weather_data import WeatherData
from app import db

"""
    Funkcja która zapisuje dane pobrane przez api następnie przetworzone przez odpowiednie do bazy danych
"""


def save_weather_data_to_db(weather_info, city, country):
    print(weather_info)
    new_data = WeatherData(
        city=city,
        country=country,
        date=datetime.now().strftime('%Y-%m-%d'),
        time=weather_info['current_time'],
        temperature=weather_info['temp'],
        humidity=weather_info['humidity'],
        rainfall=weather_info['rainfall'],
        weather=weather_info['weather'],
    )
    db.session.add(new_data)
    db.session.commit()
