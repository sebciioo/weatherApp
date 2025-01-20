import re
from .models.weather_data import WeatherData
from .utils.chart_generator import generate_chart
from .utils.data_writer import save_weather_data_to_db
from flask import Blueprint, render_template, flash, request, redirect, url_for
from .utils.weather_api_client import fetch_weather_data, fetch_air_quality_data, fetch_current_weather_data
from .utils.data_processor import process_weather_data, process_current_weather_data, process_air_quality_data, \
    process_wind_data
from .utils.geocoding import get_coordinates

main = Blueprint('main', __name__)

"""
    Function for appropriate form validation
"""


def is_valid_input(city, country):
    city_pattern = re.compile(r"^[a-zA-Z\u00C0-\u017F\s-]+$")
    country_pattern = re.compile(r"^[a-zA-Z\u00C0-\u017F\s-]+$")
    return city_pattern.match(city) and country_pattern.match(country)


"""
    Definition of routes and views for the application. Handles HTTP requests, processes forms and returns 
    appropriate responses.
"""


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city').capitalize()
        country = request.form.get('country').capitalize()
        if not is_valid_input(city, country):
            flash('Proszę wprowadzić prawidłowe miasto i kraj.', 'danger')
            return redirect(url_for('main.index'))
        return redirect(url_for('main.panel', city=city, country=country))
    return render_template('index.html')


@main.route('/panel', methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')
        if not is_valid_input(city, country):
            flash('Proszę wprowadzić prawidłowe miasto i kraj.', 'danger')
            return render_template('panel.html', city=None, country=None, weather_data=None, current_weather_data=None,
                                   air_quality_data=None, wind_data=None)
        return redirect(url_for('main.panel', city=city, country=country))

    city = request.args.get('city').capitalize()
    country = request.args.get('country').capitalize()

    """
        Once the city and country have been downloaded according to the API documentation, I convert them into the corresponding coordinates of the 
        geographic coordinates.
    """

    lat, lon = get_coordinates(city, country)
    if not lat or not lon:
        flash(f'Nie można znaleźć współrzędnych dla: {city}, {country}. Sprawdź wprowadzone dane', 'danger')
        return render_template('panel.html')

    weather_data = fetch_weather_data(lat, lon)
    current_weather_data = fetch_current_weather_data(lat, lon)
    air_quality_data = fetch_air_quality_data(lat, lon)

    """
        We then transform and select the data using the appropriate functions from data_processing
    """

    processed_weather_data = process_weather_data(weather_data) if weather_data else None
    processed_current_weather_data = process_current_weather_data(
        current_weather_data) if current_weather_data else None
    processed_air_quality_data = process_air_quality_data(air_quality_data) if air_quality_data else None
    processed_wind_data = process_wind_data(weather_data) if weather_data else None

    if not (
            processed_weather_data and processed_current_weather_data and processed_air_quality_data and processed_wind_data):
        flash('Nie udało się pobrać danych pogodowych. Spróbuj ponownie', 'danger')

    """
        Save the data to the database
    """

    save_weather_data_to_db(processed_current_weather_data, city, country)

    return render_template('panel.html', weather_data=processed_weather_data,
                           current_weather_data=processed_current_weather_data,
                           air_quality_data=processed_air_quality_data, wind_data=processed_wind_data,
                           city=city, country=country)


@main.route('/history', methods=['GET', 'POST'])
def history():
    """
        We download the data and create a list of unique cities from the database
    """
    all_weather_data = WeatherData.query.all()
    cities = list(set(data.city for data in all_weather_data))

    if request.method == 'POST':
        city = request.form.get('city')
        parameter = request.form.get('parameter')

        if not city:
            return render_template('history.html', all_weather_data=all_weather_data, cities=cities)

        """
            Retrieval of dates and values for a selected parameter from weather data
        """

        query = WeatherData.query.filter_by(city=city)
        data = query.all()

        if not data:
            return render_template('history.html', all_weather_data=all_weather_data, cities=cities)

        """
            Pobranie dat i wartości wybranego parametru z danych pogodowych
        """

        dates = [d.date for d in data]
        values = [getattr(d, parameter) for d in data]

        """
           Generation of a plot based on dates and values
        """
        chart_path = generate_chart(dates, values, parameter, city)
        chart_url = url_for('static', filename=f'chart/chart.png')

        return render_template('history.html', all_weather_data=all_weather_data, chart_url=chart_url, cities=cities)

    return render_template('history.html', all_weather_data=all_weather_data, cities=cities)
