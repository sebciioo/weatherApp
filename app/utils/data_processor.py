import calendar
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
from .transtations import weather_descriptions_translations
import matplotlib.pyplot as plt
import numpy as np
import pytz

"""
    Zawiera funkcje do przetwarzania i analizy pobranych danych pogodowych, 
    w tym obliczanie średnich wartości( np. w funkcji  process_weather_data ) i przygotowywanie danych do wyświetlania.
"""

days_of_week_translations = {
    'Monday': 'Poniedziałek',
    'Tuesday': 'Wtorek',
    'Wednesday': 'Środa',
    'Thursday': 'Czwartek',
    'Friday': 'Piątek',
    'Saturday': 'Sobota',
    'Sunday': 'Niedziela'
}


def process_weather_data(data):
    forecasts = defaultdict(lambda: {'temp': 0, 'count': 0, 'descriptions': Counter()})
    now = datetime.utcnow()
    start_time = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = now + timedelta(days=4)

    for item in data['list']:
        forecast_time = datetime.utcfromtimestamp(item['dt'])
        if forecast_time < start_time or forecast_time > end_time:
            continue
        date = forecast_time.date()
        forecasts[date]['temp'] += item['main']['temp']
        forecasts[date]['descriptions'][item['weather'][0]['description']] += 1
        forecasts[date]['count'] += 1

    daily_averages = []
    for date, values in forecasts.items():
        most_common_description = values['descriptions'].most_common(1)[0][0]
        day_of_week = calendar.day_name[date.weekday()]
        translated_day = days_of_week_translations.get(day_of_week, day_of_week)[:3]

        daily_averages.append({
            'date': date.strftime('%Y-%m-%d'),
            'avg_temperature': round(values['temp'] / values['count']),
            'day_of_week': translated_day,
            'weather': most_common_description
        })

    return daily_averages


def process_current_weather_data(data):
    dt = datetime.utcfromtimestamp(data['dt'])
    day_of_week = days_of_week_translations.get(calendar.day_name[dt.weekday()])[:3]

    local_tz = pytz.timezone('Europe/Warsaw')
    local_dt = datetime.now(local_tz).strftime('%H:%M')
    sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']).replace(tzinfo=pytz.utc).astimezone(local_tz).strftime(
        '%H:%M')
    sunset = datetime.utcfromtimestamp(data['sys']['sunset']).replace(tzinfo=pytz.utc).astimezone(local_tz).strftime(
        '%H:%M')

    rainfall = data.get('rain', {}).get('1h', 0.0)

    weather_info = {
        'temp': round(data['main']['temp']),
        'feels_like': round(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'visibility': data['visibility'],
        'sunrise': sunrise,
        'sunset': sunset,
        'day_of_week': day_of_week,
        'weather': data['weather'][0]['description'],
        'current_time': local_dt,
        'rainfall': rainfall
    }

    return weather_info


def process_air_quality_data(data):
    air_quality_info = {
        'co': round(data['list'][0]['components']['co']),
        'no': round(data['list'][0]['components']['no']),
        'pm2_5': round(data['list'][0]['components']['pm2_5']),
        'o3': round(data['list'][0]['components']['o3']),
        'aqi': data['list'][0]['main']['aqi']
    }
    return air_quality_info


def process_wind_data(data):
    wind_data = []
    local_tz = pytz.timezone('Europe/Warsaw')
    count = 0

    for item in data['list']:
        if count >= 4:
            break
        forecast_time = datetime.utcfromtimestamp(item['dt']).replace(tzinfo=pytz.utc).astimezone(local_tz)
        wind_speed = item['wind']['speed']
        wind_direction = item['wind']['deg']
        wind_data.append({
            'time': forecast_time.strftime('%H:%M'),
            'speed': wind_speed,
            'direction': wind_direction
        })
        count += 1

    return wind_data
